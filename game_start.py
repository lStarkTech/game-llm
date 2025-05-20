import pygame as py

"""esistono diversi modi per il rendering delle pixelart->
    scalare individualmente gli asset e realizzare il rendering per come appena fatto (da smoothness ma può dare problemi per altro)
    oppure, migliore per scene impegnative, è rendere la pixel art alla risoluzione minore che può e poi upscalare. Nelle nuove
    versioni di pygame può essere fatto utilizzando la flag scaled"""

py.init()
#l'angolo in alto a sinistra è nella posizione 0,0
screen = py.display.set_mode((960,540))
#surfaces, name for images in memory, everything in pygame revolves around it
#dobbiamo definire un gameloop per evitare che la finestra si chiudi automaticamente al termine dello script
"""il gameloop runna continuamente e deve controllare tutto quello che 
giri a schermo continuamente e di cui il gioco necessita, potremmo implementarlo
semplicemente con un while in cui dovremo comunque identificare un metodo per la terminazione
perché di default non terminerebbe semplicemente premendo X. """

"""sia gli eventi legati alla finestra sia quelli connessi agli input si trovano 
nel modulo event. event.get ci darà una lista di tutti gli eventi che sono avvenuti
dall'ultima volta in cui event è stato chiamato. """

"""A questo punto dobbiamo trovare un modo per poter trasformare un'immagine in una surface di pygame
    per farlo va utilizzato image.load. 
    Le surface possono avere differenti formati di pixel associati. Per utilizzare il più veloce per 
    il rendering va associato il .convert()"""

#convert_alpha dice a pygame di supportare la trasparenza dei pixel
logo = py.image.load('person.png').convert_alpha() #si deve dare un path e ci ritorna una surface del file
#se invece abbiamo uno sfondo colorato possiamo dire a pygame di ignorare quel colore
#utilizzando set_colorkey((codice rgb del colore))
logo = py.transform.scale(logo,
                      (logo.get_width()/16, logo.get_height()/16))
clock = py.time.Clock() #per modificare la velocità di update in modo tale che non vada il più velocemente possibile ma sia legato alla velocità di rendering che definiamo
x = 0
dt = 0.1
running = True;
while running:
    screen.fill((0,102,102)) #per mascherare i duplicati delle immagini a schermo che sennò si ripeterebbero
    #per inserire l'immagine a schermo:
    screen.blit(logo, (x,screen.get_height()/2))
    hitbox = py.Rect(x, screen.get_height()/2, logo.get_width(), logo.get_height())
    target = py.Rect(700, 300, 200, 200)
    collision = hitbox.colliderect(target)
    if collision:
        py.draw.rect(screen, (0,255,0), target)
    else:
        py.draw.rect(screen, (255,0,0), target)
    
    x += 60*dt
    #blit inserisce nella superficie su cui viene chiama la superficie che 
    #che è data per argomento nelle coordinate definite
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    #prende qualsiasi cosa abbiamo inserito nella screen surface e la mostra nella finestra
    py.display.flip() 
    #ritorna il tempo in millisecondi
    dt = clock.tick(60)/1000 #in questo modo però il gioco va più veloce tanto più mettiamo veloce il refresh
    #per evitare questo si conta il tempo tra i frame con un valore "delta time" e si moltiplicano gli spostamenti per questo delta time
    dt = max(0.001, min(0.1, dt))
py.quit() #per ripulire il tutto

#per modificare la dimensione di un elemento si usano le transform function

