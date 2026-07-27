import subprocess, warnings, json, os
from time import sleep

# obs: da pra criar uma classe para ser instanciada, e entao definir os devidos valores,
# coordenadas e ter metodo para executar...
# dai daria para usar esse módulo em outros projetos!
# para reseumo: ler readme

# config inicial
class ActionCfg():
    verify_precision_debug = True
    log_debugs = True

    def __init__(self, target_coord_name, move_val=20, offset=1, pointer_speed=0):
        self.target_coord_name = target_coord_name
        self.move_val = move_val
        self.offset = offset
        self.pointer_speed = pointer_speed
        # em segundos; 0 == rapido. Outro valor poderia ser 0.005 == lento

    def move_mouse(self):
        name = self.target_coord_name

        # valor da chave json selecionada
        # puxar coord de \naame do banco coordenada do nome
        obj = CfgManager.get_coordinates(name)

        for key in obj:
            coord_set = obj[key]

            # move para 1,1
            subprocess.run([
                "ydotool",
                'mousemove',
                '-x',
                '-2000',
                '-y',
                '-2000'
            ])

            # obter posi atual
            # reativar se precisar
            xy_inicial = get_current_pos()

            # print(f'\n\nDebug: Inicio ciclo para: {coord}\n')

            move_x = 0
            move_y = 0
            iterac = 0
            resto = {
                'axis': None,
                'value': 0
            }

            for target_coord in coord_set:

                for i in range(2):

                    if i == 0:
                        # print('moverá o x')
                        move_x = self.move_val
                        move_y = 0

                        iterac = target_coord['x'] / self.move_val

                        resto['value'] = (
                            target_coord['x'] - self.offset
                        ) % self.move_val

                        resto['axis'] = 'x'

                    else:
                        # print('moverá o y')
                        move_x = 0
                        move_y = self.move_val

                        iterac = target_coord['y'] / self.move_val

                        # subtrair 1 corrige o problema de passar 1 (no else tbm)
                        resto['value'] = (
                            target_coord['y'] - self.offset
                        ) % self.move_val

                        resto['axis'] = 'y'

                    # print(f'\n debug:\n iterações: {int(iterac)}\n coords:{move_x},{move_y}\n')

                    for i in range(int(iterac)):
                        subprocess.run([
                            "ydotool",
                            'mousemove',
                            '-x',
                            str(move_x),
                            '-y',
                            str(move_y)
                        ])

                        sleep(self.pointer_speed)

                    # esse tratamento do resto permite atingir a precisão;
                    # sem ele nao é preciso
                    if resto['value'] != 0:

                        if resto['axis'] == 'x':
                            subprocess.run([
                                "ydotool",
                                'mousemove',
                                '-x',
                                str(resto['value']),
                                '-y',
                                '0'
                            ])

                        else:
                            subprocess.run([
                                "ydotool",
                                'mousemove',
                                '-x',
                                '0',
                                '-y',
                                str(resto['value'])
                            ])

                sleep(target_coord['wait'])

                if target_coord['action'] == 'click':
                    CfgManager.mouse_click()

                # trecho abaixo e outro aima (xy_inicial) desativados para maior velocidade;
                # só usar pra checar precisão
                CfgManager.verify_click_precision(
                    xy_inicial=target_coord
                )

        CfgManager.debug('finalizado', 'status')


class CfgManager:

    folder = "./data"
    file_path = folder + '/db.json'

    # criar metodo para alterar config existente no json

    def get_coordinates(name=None):
        # retorna json para escolher
        db = CfgManager.get_json()

        if name == None:
            return db

        # puxa dados do nome específico
        if not name in db:

            n = input(
                'No coord with this naame, want setup?\n [y] Yes\n [n] No'
            )

            if n.lower() == 'y':
                return CfgManager.set_coorditates()

            warnings.warn(
                'NO COORD WITH THIS NAME, YOU MUST SETUP ONE; JUST RERUN'
            )

            # return None

        else:
            coordinates_cfg = db[name]
            return coordinates_cfg

            # json -->
            # {
            #     'among':[
            #         {'x':2,'y':3,'action':'click','wait':0},
            #         {'x':4,'y':5,'action':'click','wait':0}
            #     ]
            # }

    def set_coorditates():
        # adiciona dados no json

        # json, cada chave tem subchavre com as coordenadas
        name = input('[SETUP] defina o nome da configuração: ')

        coord = []

        for i in range(10):

            print('\n[SETUP] COORDENADA {i+1}')

            x = int(input(f'\n insira o valor de x: '))
            y = int(input(f'\n insira o valor de y: '))

            action = input(
                '\n insira o tipo de ação [default=click]'
            )

            action = 'click' if action == '' else action

            try:
                wait = int(
                    input('Valor de wait [default=0]: ')
                )

            except ValueError:
                wait = 0

            # add pointer speed e resto
            coord.append({
                'x': x,
                'y': y,
                'wait': wait
            })

            cont = input(
                '\n\n[WARN] adicionar outras coordenadas? [y] ou [n]'
            )

            if cont.lower() == 'n':
                break

        new_db_data = {
            name: [
                {
                    'x': x,
                    'y': y,
                    'wait': wait,
                    'action': action
                }
            ]
        }

        CfgManager.set_json(new_db_data)

        return new_db_data

        # faz get de todas e adiciona a nova

        pass

    def get_json():
        # puxa json, cria se nao existir em ./data

        os.makedirs(CfgManager.folder, exist_ok=True)

        db = {}

        try:
            with open(CfgManager.file_path, 'r') as file:
                db = json.load(file)

        except:
            with open(
                CfgManager.file_path,
                'w',
                encoding='utf-8'
            ) as file:

                json.dump(
                    db,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        return db

    def set_json(new_dict):
        # recebe novo objeto com nova chave + valores
        # atualiza/salva json

        os.makedirs(CfgManager.folder, exist_ok=True)

        db = CfgManager.get_json()

        for i in new_dict:
            db[i] = new_dict[i]

        with open(
            CfgManager.file_path,
            'w',
            encoding='utf-8'
        ) as file:

            json.dump(
                db,
                file,
                ensure_ascii=False,
                indent=4
            )

    def verify_click_precision(xy_inicial):

        if not ActionCfg.verify_precision_debug and not ActionCfg.log_debugs:
            return

        xy_final = CfgManager.get_current_pos()

        x = xy_inicial['x'] - xy_final['x']
        y = xy_inicial['y'] - xy_final['y']

        CfgManager.debug(
            f"coord inicial: {xy_inicial['x']},{xy_inicial['y']}\n"
            f"coord final: {xy_final['x']},{xy_final['y']}\n"
            f"precision: {x},{y}",
            'debug'
        )

    def debug(msg, type):

        if type == 'status':
            print(f'\n[STATUS]: {msg}')

        # obs: se log debugs estiver desativado mas verif precision for true,
        # ele debuga; dai n precisa alterar var/config, o script o faz

        elif (
            type == 'debug'
            and ActionCfg.log_debugs
        ) or ActionCfg.verify_precision_debug:

            print(f'\n[DEBUG ON]:\n {msg}')

        else:
            warnings.warn(
                f'parameto de debug inválidio: {type}',
                DeprecationWarning
            )

    def mouse_click():
        subprocess.run(
            ["ydotool", "click", "0xC0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def get_current_pos():

        proc = subprocess.Popen(
            ["slurp", "-p"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        sleep(1.5)

        # clique para obter coord cursor pelo slurp
        CfgManager.mouse_click()

        sleep(1)

        # recebe saida do slurp -p (coordenadas + outras infos)
        stdout, _ = proc.communicate()

        # pega apenas coordenadas
        coord = stdout.split()[0]  # "123,456"

        current_x, current_y = map(
            int,
            coord.split(",")
        )

        return {
            'x': current_x,
            'y': current_y
        }


# exemplo; wait em segundos; tempo para iniciar novo clique
#
# coordenadas = [
#     {"x": 1297, "y": 18, 'wait':1.2, 'action':'click'},
#     {"x": 1187, "y": 46, 'wait':1.2, 'action':'click'},
# ]
#
# resumo lá em cima
#
# ActionCfg.move_mouse()
