from llm_npc import LLM_NPC
import pygame

"""Da ricordare. Gemma3:1b è troppo piccolo, non risce a capire le richieste e continua a fare le funzioni con print.
Gemma3:4b è il modello che funziona meglio, ma ancora non mi restituisce il formato corretto delle funzioni.
codegemma invece non è completamente in grado di capire le richieste, ma è molto più veloce.
quen2.5-coder:7b è il modello che funziona meglio, ma è più lento, per quanto non così eccessivamente di più rispetto
a gemma3:4b."""

while True:
    pygame.init()
    npc = LLM_NPC()
    user_input = input("Enter your command: ")
    if user_input.lower() == "exit":
        npc.ollama_process.terminate()
        print("Exiting the NPC interaction.")   
        break

    function_code = ""  
    print("npc:", end=" ", flush=True)
    for token in npc.chain.stream({"input": user_input}):
        print(token, end='', flush=True)
        function_code += token
    function_code = function_code.replace("`", '')
    function_code = function_code.replace("python", "")
        
    print()
    print(function_code)
    with open("debug_function_code.py", "w", encoding="utf-8") as f:
        f.write(function_code)
    try:
        exec(function_code, globals())
        print("Exec is working")

    except Exception as e:
        print(f"Exec is not working: {e}")
