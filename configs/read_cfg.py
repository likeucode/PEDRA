# Author: Aqeel Anwar(ICSRL)
# Created: 9/20/2019, 12:43 PM
# Email: aqeel.anwar@gatech.edu

import configparser as cp
from dotmap import DotMap
import os, json

def read_env_cfg(config_filename = 'configs/main.cfg'):
    # Load from config file
    cfg = DotMap()

    config = cp.ConfigParser()
    config.read(config_filename)

    cfg.run_name = config.get('general_params', 'env_name')
    cfg.floorplan = str(config.get('general_params', 'floorplan'))
    cfg.o_x = float(config.get('general_params', 'o_x').split(',')[0])
    cfg.o_y = float(config.get('general_params', 'o_y').split(',')[0])
    cfg.alpha = float(config.get('general_params', 'alpha').split(',')[0])
    cfg.ceiling_z = float(config.get('general_params', 'ceiling_z').split(',')[0])
    cfg.floor_z = float(config.get('general_params', 'floor_z').split(',')[0])
    cfg.player_start_z = float(config.get('general_params', 'player_start_z').split(',')[0])

    return cfg

def generate_json(cfg):
    path = os.path.expanduser('~\Documents\Airsim')
    if not os.path.exists(path):
        os.makedirs(path)

    filename = path + '\settings.json'

    data = {}
    data['SettingsVersion'] = 1.2
    data['LocalHostIp'] = cfg.ip_address
    data['SimMode'] = cfg.SimMode
    data['ClockSpeed'] = cfg.ClockSpeed

    PawnPaths = {}
    PawnPaths["DefaultQuadrotor"] = {}
    PawnPaths["DefaultQuadrotor"]['PawnBP'] = ''' Class'/AirSim/Blueprints/BP_''' + cfg.drone + '''.BP_''' + cfg.drone + '''_C' '''
    data['PawnPaths']=PawnPaths

    data['CameraDefaults'] = []
    CaptureSettings=[]

    camera = {}
    camera['ImageType'] = 0
    camera['Width'] = cfg.width
    camera['Height'] = cfg.height
    camera['FOV_degrees'] = cfg.fov_degree
    CaptureSettings.append(camera)
    data['CameraDefaults'].append(CaptureSettings)
    camera['ImageType'] = 3
    data['CameraDefaults'].append(CaptureSettings)
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)




def read_cfg(config_filename = 'configs/main.cfg', verbose = False):
    # Load from config file
    cfg = DotMap()

    config = cp.ConfigParser()
    config.read(config_filename)

    cfg.run_name = config.get('general_params', 'run_name')
    if str(config.get('general_params', 'custom_load')) =='True':
        cfg.custom_load = True
    else:
        cfg.custom_load = False
    cfg.custom_load_path = str(config.get('general_params', 'custom_load_path'))
    cfg.env_type = config.get('general_params', 'env_type')
    cfg.env_name = config.get('general_params', 'env_name')
    cfg.phase = config.get('general_params', 'phase')
    cfg.SimMode = str(config.get('general_params', 'SimMode'))
    cfg.drone = str(config.get('general_params', 'drone'))
    cfg.ClockSpeed = int(config.get('general_params', 'ClockSpeed').split(',')[0])
    # [Simulation Parameters]
    if str(config.get('simulation_params', 'load_data')) =='True':
        cfg.load_data = True
    else:
        cfg.load_data = False
    cfg.load_data_path = str(config.get('simulation_params', 'load_data_path'))
    cfg.ip_address = str(config.get('simulation_params', 'ip_address'))


    # [Camera_params]
    cfg.width = int(config.get('camera_params', 'width').split(',')[0])
    cfg.height = int(config.get('camera_params', 'height').split(',')[0])
    cfg.fov_degrees = int(config.get('camera_params', 'fov_degrees').split(',')[0])


    # [RL Parameters]
    cfg.input_size = int(config.get('RL_params', 'input_size').split(',')[0])
    cfg.num_actions = int(config.get('RL_params', 'num_actions').split(',')[0])
    cfg.train_type = config.get('RL_params', 'train_type')
    cfg.wait_before_train = int(config.get('RL_params', 'wait_before_train').split(',')[0])
    cfg.max_iters = int(config.get('RL_params', 'max_iters').split(',')[0])
    cfg.buffer_len = int(config.get('RL_params', 'buffer_len').split(',')[0])
    cfg.batch_size = int(config.get('RL_params', 'batch_size').split(',')[0])
    cfg.epsilon_saturation = int(config.get('RL_params', 'epsilon_saturation').split(',')[0])
    cfg.crash_thresh = float(config.get('RL_params', 'crash_thresh').split(',')[0])
    cfg.gamma = float(config.get('RL_params', 'gamma').split(',')[0])
    cfg.dropout_rate = float(config.get('RL_params', 'dropout_rate').split(',')[0])
    cfg.lr = float(config.get('RL_params', 'learning_rate').split(',')[0])
    cfg.switch_env_steps = int(config.get('RL_params', 'switch_env_steps').split(',')[0])
    cfg.epsilon_model = config.get('RL_params', 'epsilon_model')
    cfg.Q_clip = bool(config.get('RL_params', 'Q_clip'))
    cfg.train_interval = int(config.get('RL_params', 'train_interval').split(',')[0])
    cfg.update_target_interval = int(config.get('RL_params', 'update_target_interval').split(',')[0])


    if verbose and cfg.phase=='train':
        print('------------------------------ Config File ------------------------------')
        for param in cfg:
            spaces = ' '*(30-len(param))
            print(param+':'+spaces + str(cfg[param]))

    # print('-------------------------------------------------------------------------')
    print()
    return cfg

