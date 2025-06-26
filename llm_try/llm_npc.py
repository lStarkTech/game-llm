
import subprocess
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory

class LLM_NPC:
    def __init__(self, model_name: str = "qwen2.5-coder:7b"):
        self.model_name = model_name
        # Start the Ollama server
        #self.ollama_process = subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Wait for the process to start
        self.llm = OllamaLLM(model=self.model_name, stream = True)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system","""You have to generate python functions, using the pygame library, that will be executed in a game.
             The functions must be in the format:
             def key_that_must_be_pressed_to_execute_the_action(player, game_state):
             the player is an object of the class Player with the following attributes:
             - player.rect: the rectangle of the player, used for collision detection.
             - player.visual_rect: the rectangle of the player, used for drawing the player on the screen.
             - player.state: the state of the player, can be "idle", "running", "jumping", "falling".
             - player.facing_right: a boolean that indicates if the player is facing right or left.
             - player.animations: a dictionary with the animations of the player, with the following keys:
             - "idle": the idle animation of the player.
             - "run": the running animation of the player.
             - player.speed: the speed of the player, used to move the player.
             The game_state is a string that indicates the state of the game, can be "intro", "game", "pause", "game_over".
             Only write the function, without any other text.
             """),
            ("user", "{input}"),
        ])
        self.chain = self.prompt_template | self.llm



        



    def generate_response(self, user_input: str) -> str:
        prompt = self.prompt_template.format(input=user_input)
        response = self.llm(prompt)
        return response.content

