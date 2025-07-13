from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import os #ci serve per poter controllare che il file esista e per poter, successivamente far avviare dal codice ollama come subprocess
import ast #serve per controllare la sintassi del codice generato
import importlib.util #serve per poter importare dinamicamente il file dei controlli che verrà generato dal LLM
import time
import copy


class GameLLMController:

    def __init__(self, model_name: str = "hermes3:8b", controls_file: str = "LLM_Controls.py", game_context: dict = None):
        self.model_name = model_name
        self.controls_file = controls_file
        self.dynamic_module = None
        """Individua il contesto del gioco, ovvero gli oggetti che gli sarà permesso toccare. 
        Il giocatore, nel caso eventuali nemici, bottoni, porte... serve??"""
        self.game_context = game_context
        """Definiamo un dizionario che contenga le funzioni generate dalla LLM e che potranno essere invocate
        durante l'esecuzione del gioco. Il rioconoscimento in questo momento verrà fatto mediante i tasti che richiederanno"""
        self.key_functions: dict[str, callable] = {}
        self.llm = OllamaLLM(model=self.model_name, stream = True)
        self._init_controls_file() #inizializza il file dei controlli se non esiste già
        

    def set_game_context(self, player_obj, game_objects_list):
        """Funzione per impostare il contesto del gioco, in modo che le funzioni
        generate dal LLM possano accedere agli oggetti del gioco."""
        self.game_context = {
            "player": player_obj,
            "game_objects": game_objects_list,
            #"dt": delta_time
        }
        #dobbiamo richiamare la funzione set_game_context all'interno del file dei controlli per poter aggiornare il contesto
        try:
            spec = importlib.util.spec_from_file_location("LLM_Controls", self.controls_file)
            self.dynamic_module= importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.dynamic_module)
            self.dynamic_module.set_game_context(player_obj, game_objects_list)
        except Exception as e:
            print(f"Error setting game context: {e}")

    def update_game_context(self, player_obj, game_objects_list):
        if self.dynamic_module is None:
            print("Dynamic module has not been initialized")
            return
        try:
            self.dynamic_module.set_game_context(player_obj, game_objects_list)
        except Exception as e:
            print(f"Error updating game context: {e}")

#dobbiamo qua inserire il contesto del gioco che dovrà impiegare e poter utilizzare per la generazione delle funzioni
    def _init_controls_file(self):
        """controlla se il file sia già stato creato e in caso contrario inizializza
        il file inserendo degli elementi di base per descrivere anche a cosa serva il file stesso."""
        if not os.path.exists(self.controls_file):
            inizio_file ='''"""File in cui verranno inserite le funzioni create dal LLM"""
            """Nonostante sia migliore non inserire delle variabili globali, per evitare che il LLM dimentichi di prendere
            gli elementi corretti, li mettiamo come globali per essere comunque accessibili"""
            import pygame
            import math #importato nel caso in cui definisse la fisica di gioco in maniera "realistica"
            import collision

            player = None #prenderà l'oggetto player per poterlo "manipolare"
            game_objects = None #prenderà gli oggetti del gioco con cui il player può interagire
            #dt = 0 #prenderà il delta time del gioco per poter calcolare le velocità e le accelerazioni


            #funzione che verrà richiamata nel main del gameloop
            def set_game_context(player_obj, game_objects_list):
                """Funzione per impostare il contesto del gioco, in modo che le funzioni
                generate dal LLM possano accedere agli oggetti del gioco."""
                global player, game_objects, dt
                player = player_obj
                game_objects = game_objects_list
                #dt = delta_time
            ''' 
            #se il file deve essere creato, allora gli scriviamo la parte iniziale che è fondamentale
            with open(self.controls_file, 'w') as file:
                file.write(inizio_file)

#carica i controlli presenti all'interno del file sul dizionario
    def load_written_controls(self):
        """Carica, se esistono, le funzioni di controllo scritte dal LLM"""
        try: 
            #controlliamo innanzitutto se il modulo dinamico sia stato correttamente caricato
            if self.dynamic_module is None:
                print(f"Dynamic module has not been loaded.")
                return
            
            """Cerchiamo all'interno del modulo caricato dinamicamente tutte le funzioni che, teoricamente, sono state chiamate in maniera corretta
            dal LLM, ovvero nello stile di pygame, e le inseriamo all'interno di un dizionario con il quale poterle richiamare tramite 
            self.key_functions[function_name]() quando necessario."""
            for function_name in dir(self.dynamic_module):
                if function_name.startswith("K_") and callable(getattr(self.dynamic_module, function_name)):
                    self.key_functions[function_name] = getattr(self.dynamic_module, function_name)
            print(f"Loaded controls: {list(self.key_functions.keys())}")

        except Exception as e:
            print(f"Error loading controls: {e}")


    def remove_control(self, key: str):
        """rimuove la vecchia definizione della funzione all'interno del file dei controlli"""
        if "K_"+key in self.key_functions:
            del self.key_functions["K_"+key]
        
        if not os.path.exists(self.controls_file):
            print(f"Controls file {self.controls_file} does not exist. Cannot remove control.")
            return
        
        with open(self.controls_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        skip = False
        for line in lines:
            if line.strip().startswith(f"def K_{key}("):
                skip = True  # inizia a saltare
                continue
            if skip and line.strip().startswith("def "):  # trovata un'altra funzione
                skip = False
            if not skip:
                new_lines.append(line)

        with open(self.controls_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

#controllare se ha senso il key string in quanto teoricamente dovrebbe essere detto dal giocatore e quindi far parte dell'input
    def controls_generation(self, user_input: str, key: str):
        """Si occupa di generare la funzione in base all'input richiesto dal giocatore e al
        tasto che dovrà essere premuto per eseguire l'azione."""

        """definiamo il prompt che verrà impiegato. In realtà potremmo anche sfruttare il prompt dentro ollama per poter impiegare un modello 'personalizzato'
        per questo esatto scopo. Per farlo però vi è bisogno di assicurarci che il prompt funzioni correttamente, sennò non porterebbe a nulla e sarebbe
        solo un casino ogni volta da modificare"""
        try:
            prompt = PromptTemplate.from_template("""
                        You are a code generator for a 2D platformer game built using Python and Pygame.
                        Your task is to write a function that will be called when the player presses the key "{key}".
                        The user has requested the following behavior: "{user_input}"

                        ### CONTEXT

                        You can access the following global variables:
                        - player: the Player object
                        - game_objects: a list of interactive objects (like colliders, ladders, doors, and buttons)
                        - collision.handle_collision(player, game_objects): call to handle collisions
                                                  
                        ### PLAYER OBJECT STRUCTURE

                        The player object has the following attributes:
                        - player.rect: pygame.Rect, for collisions and movement
                        - player.visual_rect: pygame.Rect, used for rendering
                        - player.state: string, must be either "idle" or "running", must be set when the player moves
                        - player.facing_right: boolean, direction the player is facing. Important during movements
                        - player.speed: float, movement speed
                        - player.velocity_y: The current vertical speed.
                        - player.gravity: Constant vertical acceleration.
                        - player.jump_power: Initial negative impulse for jumping.
                        - player.on_ground: True if touching ground, needed for jumps to happen.
                        - player.dx : the current orizontal movement that needs to be applied to the player
                        ### GAME OBJECT TYPES

                        In the game_objects list, you will find:
                        - rects (they are the objects for collisions)


                        ### PHYSICS AND RULES

                        - You MUST use `player.rect.x += ...` or `.y += ...` to move.
                        - For horizontal movement, assign `player.dx = ±player.speed`
                        - You CAN'T make the player "run" or "move" up and down, only jump or fly on the Y axe. 
                        - Do NOT assign or use any attribute not explicitly listed above.
                        - Do NOT create new player states other than "idle" or "running".
                        - the player must be in "idle" only when it is not moving
                        - After applying movement, ALWAYS call: collision.handle_collision(player, game_objects)
                        - Do NOT try to use other variables that are not listed here
                        - Do NOT print or log any information.
                        - Do NOT access external resources or use global imports.

                        You must implement the full behavior in your function. 
                        If the action (like jumping, flying, or falling) requires frame-by-frame evolution, you must implement a continuous behavior manually:

                        - Use player.velocity_y and player.gravity to simulate jumping and falling.
                        - remember to use player.speed and player.dx for left and right movements
                        - Apply movement using player.rect.y += ...
                        - remember to consider even the player.visual_rect.

                        You are NOT allowed to assume the game handles gravity or jumping on its own.

                        ### OUTPUT FORMAT

                        Write ONLY the function definition, named exactly: `K_{key}`
                        Do NOT write any other text, comments, or explanations.
                        The function must:
                        - take no arguments
                        - modify only allowed attributes or objects
                        - execute cleanly when bound to a keypress
                                                """)

            chain = prompt | self.llm
        
            try:
                start_time = time.perf_counter()
                response = chain.invoke({"user_input": user_input, "key": key})
                function_code = response.content if hasattr(response, "content") else response
                print(f"Generated code for {key}:\n{function_code}")
                validated_code = self.validate_generated_code(function_code, key)
                
                if validated_code is None:
                    print(f"Generated code for {key} is invalid. Please try again.")
                    end_time = time.perf_counter()
                    generation_time = end_time - start_time
                    print(f"Tempo trascorso: {generation_time:.2f} secondi")
                    return None
                #scriviamo intanto il codice generato all'interno del .py in modo da poter ricaricare ad apertura del gioco tutte le funzioni create
                #nel caso in cui si debba sovrascrivere il tasto, rimuoviamo la vecchia funzione
               
                self.remove_control(key)
             
                new_function = self.load_new_control(validated_code, key)
                if new_function is None:
                    print(f"Failed to load the new function {key}.")
                    end_time = time.perf_counter()
                    generation_time = end_time - start_time
                    print(f"Tempo trascorso: {generation_time:.2f} secondi")
                    return None
                self.key_functions["K_"+key] = new_function
                with open(self.controls_file, 'a', encoding='utf-8') as file:
                    file.write("\n" + validated_code + "\n")  # i \n sono inseriti per assicurare la separazione tra le funzioni
                print(f"Function {key} generated and saved successfully.")
                end_time = time.perf_counter()
                generation_time = end_time - start_time
                print(f"Tempo trascorso: {generation_time:.2f} secondi") #mostra il tempo necessario alla velocità di una singola funzione da parte del modellos
   
                return new_function
                """Una volta che il codice è stato validato, dobbiamo inserirlo all'interno del dizionario."""
            except Exception as e:
                print(f"Error generating function {key}: {e}")
                return None
        except Exception as e:
            print(f"Error in chain generation: {e}")
            return None              


    def load_new_control(self, validated_code: str, function_key: str) -> callable:
        """metodo per caricare una nuova funzione creata dal LLM a runtime"""
        try:
            """testiamo la funzione su una copia degli elementi in modo che non vengano realmente toccati in caso di incorrettezza"""
            test_player = copy.deepcopy(self.dynamic_module.player)
            test_objects = copy.deepcopy(self.dynamic_module.game_objects)
            test_local_env = {}
            test_globals ={
                "pygame": __import__("pygame"),
                "collision": __import__("collision"),
                "player": test_player,  
                "game_objects": test_objects,  

            }

            exec(validated_code, test_globals, test_local_env)
            test_func = test_local_env.get("K_"+function_key)

            if not callable(test_func):
                print(f"The function K_{function_key} was not correctly written")
                return None
            try:
                test_func()
            except Exception as e:
                    print(f"The generated function K_{function_key} is not correct")
                    return None
            
            #creiamo un dizionario che verrà impiegato per contenere quanto eseguito dalla exec, in modo da ottenere il nostro callable
            local_env = {}
            needed_globals = {
                "pygame": __import__("pygame"),
                "collision": __import__("collision"),
                "player": self.dynamic_module.player,  
                "game_objects": self.dynamic_module.game_objects,  
            }
            exec(validated_code, needed_globals, local_env)
            return local_env.get("K_"+function_key)

        except Exception as e:
            print(f"Error executing code: {e}")
            return None

    def validate_generated_code(self, code: str, requested_key: str) -> str:
        """Validates the generated code using AST parsing."""
        try:
            #effettuiamo una pulizia del codice scritto in caso di presenza di componenti inutili che potrebbero non far eseguire il codice
            
            if "```python" in code:
                code = code.split("```python", 1)[-1]
            if "```" in code:
                code = code.split("```", 1)[0]
            code = code.strip()
        
        #a questo punto controlliamo che il codice sia valido 
            try:
                ast.parse(code)

            except SyntaxError as e:
                print(f"Syntax error in generated code: {e}")
                return None

            if f"def K_{requested_key}(" not in code:
                print(f"Generated code does not define a function named {requested_key}.")
                return None
            
            return code

        except Exception as e:
            print(f"Error validating generated code: {e}")
            return None
        

    def function_reload(self, player_obj, game_objects):
        self.key_functions.clear() #punliamo il dizionario in modo da evitare riferimenti doppi
        self.set_game_context(player_obj, game_objects) #ricarichiamo il modulo dinamico in modo da riottenere anche le funzioni scritte durante il gioco
        self.load_written_controls() #ricarichiamo effettivamente i controlli definiti in modo da averli
