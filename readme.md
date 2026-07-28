# Dependencias
- ferramenta ydotool instalada
       -necessário configurar grupo input (add o user e add rules; pesquisar!)

- servidor ydotoold rodando (o script o iniciará se não estiver rodando; importante ao terminar o uso rodar "sudo pkill ydotoold")
- (importante primeiro uso do ydotool) 
	-na primeira execução, rode no terminal ydotoold (para o "mouse" ser criado) e pode pressionar ctrl+c
	-desativar aceleração do ponteiro em settings -> mouse -> selecinar device "ydotool (...)" -> desmarcar aceleração do ponteiro -> aplicar

# uso:
import click_on as cl
cl.clickOn(1224,53)
cl.click_on(187, 460)

obs: certifique de rodar "sudo pkill ydotoold" após terminar de usar!
