import requests , os , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re , socket , threading , ssl , pytz , aiohttp , uuid 
from protobuf_parser import Parser
from xC4 import * ; from xHeaders import *
from xC4 import GeT_Ban_Status
from xC4 import get_player_info, get_player_bio, get_player_name, save_bot_token_to_file, get_player_full_info
from datetime import datetime
from groq import Groq
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2, data_pb2, uid_generator_pb2
from cfonts import render, say
import traceback
import random 
import asyncio
import aiohttp
import json

# =========================================================
# LOGIN CREDENTIALS - Set whatever is available
# =========================================================

ACCESS_TOKEN = '763ba96d9e1686cedefb25e6460cc83f015bcdba662b995e43985b215de197a5' 

UID      = '5107265989'
PASSWORD = '36E45ECE28695F0ACC8267AE27896093B098D6F401F5B5FC51BDA141AFB551BF'

# =========================================================
# GLOBAL VARIABLES
# =========================================================
AUTO_FRIEND_REQUEST_UIDS = [
35427788, 11367576316, 6984021410, 3669610876, 1076551119
]

Chat_Leave = False
joining_team = False
insquad = None
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_a = False
uid = None
room_uid = None
response = None
inPuTMsG = None
chat_id = None
data = None
data2 = None
key = None
iv = None
STATUS = None
AutHToKen = None
OnLineiP = None
OnLineporT = None
ChaTiP = None
ChaTporT = None
LoGinDaTaUncRypTinG = None
XX = None
sent_inv = None
lag_running = False
lag_task = None
bundle_trigger_id = None
active_tasks = []
BUNDLE_IDS = [914047001]
ai_memory = {}
AI_MODE = False # Track AI mode status
BOT_UID = None   # Track bot's own UID to avoid reading own messages
spam_room_active = False  # Room spam running flag
room_spam_task = None  # Room spam async task



# =========================================================
# EMOTE SYSTEM
# =========================================================
EMOTE_IDS_LIST = [
    909000063, 909000068, 909000075, 909000081,
    909000085, 909000090, 909000098, 909033001,
    909033002, 909035007, 909035012, 909038009,
    909038010, 909039011, 909040010, 909041005,
    909042008
]


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB53"
}

# =========================================================
# PURPLE GRADIENT LOGO SECTION
# =========================================================
def get_purple_gradient(text):
    """
    Purple, Violet aur Magenta ka ek premium aur shiny gradient transition.
    """
    result = ""
    lines = text.splitlines()
    for line_idx, line in enumerate(lines):
        # Vertical flow ke liye offset
        row_offset = line_idx * 2.0
        
        for char_idx, char in enumerate(line):
            
            r = int(max(100, min(255, 120 + (row_offset + char_idx) * 2)))
            g = int(max(0, min(50, 50 - (row_offset + char_idx))))
            b = 255 # Blue component high rakha hai purplish look ke liye
            
            # Bold + RGB ANSI
            result += f"\033[1m\033[38;2;{r};{g};{b}m{char}"
        result += "\n"
    return result

def show_logo():
    """Display purple gradient logo"""
    raw_logo = r"""
 __      ___                            
 \ \    / (_)                           
  \ \  / / _ _ __  _ __  _   _ _   _ _   _ 
   \ \/ / | | '_ \| '_ \| | | | | | | | | |
    \  /  | | | | | | | | |_| | |_| | |_| |
     \/   |_|_| |_|_| |_|\__, |\__, |\__, |
                          __/ | __/ | __/ |
                         |___/ |___/ |___/ """
    
    purple_logo = get_purple_gradient(raw_logo)
    print(purple_logo)
    
    # Branding line under logo
    print(f"           \033[1m\033[33mTelegram:\033[0m \033[1m\033[37m@the_vinnyyy\033[0m")
    print(f"      \033[37m____________________________________\033[0m\n")

# =========================================================
# UTILITY FUNCTIONS
# =========================================================
def get_random_color():
    colors = ["[FFFFFF]"]
    return random.choice(colors)

def get_random_message():
    messages = [ "Hello", "hey", "hlw", "hii", "hmm bolo" , "hmm" , "hmm kaise ho?"
    ]
    return random.choice(messages)

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)
    return False

async def PeriodicStateReset():
    global insquad, joining_team
    while True:
        await asyncio.sleep(3)
        if insquad is not None and joining_team is False:
            insquad = None

        
# =========================================================
# ENCRYPTION/DECRYPTION FUNCTIONS
# =========================================================
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"

    headers = {
        'User-Agent': 'GarenaMSDK/4.0.19P9',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    data = {
        'uid': uid,
        'password': password,
        'response_type': 'token',
        'client_type': '2',
        'client_secret': '2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3',
        'client_id': '100067'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data, timeout=5) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result.get('open_id'), result.get('access_token'), result.get('platform', 4)
                return None, None, None
    except Exception as e:
        print(f"    ⚠️ Token request error: {e}")
        return None, None, None

async def InSpeCcToKeN(access_token):
    url = f"https://100067.connect.garena.com/oauth/token/inspect?token={access_token}"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                print(f"[!] Token inspect failed: HTTP {response.status}")
                return (None, None)
            data = await response.json()
            if 'error' in data:
                print(f"[!] Token invalid: {data.get('error')}")
                return (None, None)
            open_id  = data.get("open_id")
            platform = data.get("platform", 4)
            print(f"[✓] Open ID  : {open_id}")
            print(f"[✓] Platform : {platform}")
            return (open_id, platform) if open_id else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token, platform=4):

    platform_str = str(platform)
    platform_int = int(platform)

    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 2
    major_login.client_version = "1.123.2"
    major_login.client_version_code = "2024010012"
    major_login.system_software = "Android OS 11 / API-30 (RQ3A.210805.001)"
    major_login.system_hardware = "Handheld"
    major_login.device_type = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_operator_a = "Verizon"
    major_login.network_type = "WIFI"
    major_login.network_type_a = "WIFI"
    major_login.screen_width = 1080
    major_login.screen_height = 2400
    major_login.screen_dpi = "440"
    major_login.processor_details = "ARMv8"
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.memory = 6144
    major_login.gpu_renderer = "Adreno (TM) 650"
    major_login.gpu_version = "OpenGL ES 3.2 V@1.50"
    major_login.graphics_api = "OpenGLES3"
    major_login.unique_device_id = f"Google|{uuid.uuid4()}"
    major_login.client_ip = ""
    major_login.language = "en"
    major_login.open_id = open_id
    
    # Dynamic Platform Constraints:
    major_login.open_id_type = platform_str
    major_login.login_open_id_type = platform_int
    major_login.origin_platform_type = platform_str
    major_login.primary_platform_type = platform_str
    
    major_login.access_token = access_token
    major_login.login_by = 3
    major_login.platform_sdk_id = 2
    
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    
    major_login.external_storage_total = 128512
    major_login.external_storage_available = random.randint(38000, 52000)
    major_login.internal_storage_total = 110731
    major_login.internal_storage_available = random.randint(18000, 32000)
    major_login.game_disk_storage_total = 26628
    major_login.game_disk_storage_available = random.randint(18000, 25000)
    major_login.external_sdcard_total_storage = 119234
    major_login.external_sdcard_avail_storage = random.randint(25000, 60000)
    
    major_login.library_path = "/data/app/~~random/base.apk"
    major_login.library_token = "hash|base.apk"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.supported_astc_bitset = 16383
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = random.randint(9000, 18000)
    major_login.release_channel = "android"
    major_login.channel_type = 3
    major_login.reg_avatar = 1
    major_login.if_push = 1
    major_login.is_vpn = 0
    major_login.android_engine_init_flag = 110009
    
    string = major_login.SerializeToString()
    return await encrypted_proto(string)


async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization'] = f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto

async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9:
        headers = '0000000'
    elif uid_length == 8:
        headers = '00000000'
    elif uid_length == 10:
        headers = '000000'
    elif uid_length == 7:
        headers = '000000000'
    else:
        print('Unexpected length')
        headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

async def cHTypE(H):
    if not H:
        return 'Squid'
    elif H == 1:
        return 'CLan'
    elif H == 2:
        return 'PrivaTe'

async def SEndMsG(H, message, Uid, chat_id, key, iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid':
        msg_packet = await xSEndMsgsQ(message, chat_id, key, iv)
    elif TypE == 'CLan':
        msg_packet = await xSEndMsg(message, 1, chat_id, chat_id, key, iv)
    elif TypE == 'PrivaTe':
        msg_packet = await xSEndMsg(message, 2, Uid, Uid, key, iv)
    return msg_packet

async def SEndPacKeT(OnLinE, ChaT, TypE, PacKeT):
    if TypE == 'ChaT' and ChaT:
        whisper_writer.write(PacKeT)
        await whisper_writer.drain()
    elif TypE == 'OnLine' and OnLinE:
        online_writer.write(PacKeT)
        await online_writer.drain()

# =========================================================
# SPAM FUNCTIONS
# =========================================================
async def spam_request(sender_uid, target_uid, room_id, delay, key, iv, region):
    global spam_room, spammer_uid, online_writer, whisper_writer, uid 

    if spammer_uid != target_uid or not spam_room:
        return

    print(f"Starting Invite POP-UP spam (Continuous Mode) to {target_uid} with delay {delay}s.")
    
    try:
        while spam_room and spammer_uid == target_uid:
            
            try:
                if not online_writer:
                    raise Exception("Online connection (online_writer) is not active.")

                P_Sq = await OpEnSq(key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', P_Sq)

                P_Inv = await SEnd_Inv_R(sender_uid, target_uid, key, iv) 
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', P_Inv) 
                
                await asyncio.sleep(delay)
                
            except Exception as e:
                print(f"Temporary Spam Error (will retry in 1s): {e}")
                await asyncio.sleep(1) 
                continue

    except Exception as final_e:

        print(f"Critical Spam Error: {final_e}")
        pass
    
    print(f"Invite POP-UP spam finished/stopped for {target_uid}.")
    spam_room = False
    spammer_uid = None
    
async def lag_team_loop(team_code, key, iv, region):
    global lag_running, whisper_writer, online_writer    
    print(f"⚡ Starting simple lag attack: {team_code}")    
    start_time = time.time()    
    try:
        while lag_running and (time.time() - start_time) < 59:
            try:
                # JOIN squad
                join_packet = await GenJoinSquadsPacket(team_code, key, iv)
                if online_writer and whisper_writer:
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                
                await asyncio.sleep(0.01)  # 50ms

                exit_packet = await ExiT(uid, key, iv)  # uid is global
                if online_writer and whisper_writer:
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', exit_packet)
                
                await asyncio.sleep(0.01)  # 50ms
                
            except Exception as e:
                print(f"⚠️ Lag cycle error: {e}")
                await asyncio.sleep(0.1)
        
        print(f"✅ Lag attack completed after 30 seconds")
        
    except Exception as e:
        print(f"❌ Lag attack error: {e}")
    finally:
        lag_running = False
        
        
async def execute_kick_action(target_uid, chat_type, current_uid, chat_id, key, iv):
    global whisper_writer, online_writer # Dono ko global le lo
    try:
        from xC4 import KickTarget
        kick_packet = await KickTarget(target_uid, key, iv)
        
        if kick_packet:
            if isinstance(kick_packet, str):
                kick_packet = bytes.fromhex(kick_packet)
            if online_writer:
                online_writer.write(kick_packet)
                await online_writer.drain()
                print(f"DEBUG: Packet sent via online_writer to {target_uid}")
            if whisper_writer:
                whisper_writer.write(kick_packet)
                await whisper_writer.drain()
                print(f"DEBUG: Packet sent via whisper_writer to {target_uid}")

            success_msg = f"[B][C][00FF00]✅ Kick Request Sent for {target_uid}!"
            await safe_send_message(chat_type, success_msg, current_uid, chat_id, key, iv)
            
        else:
            print("❌ Error: Packet generate hi nahi hua!")

    except Exception as e:
        print(f"❌ Kick Execution Failed: {e}")


async def send_paged_help(pages, chat_type, uid, chat_id, key, iv):
    try:
        for page in pages:
            # Har page (message) ko ek ke baad ek bhejega
            await safe_send_message(chat_type, page, uid, chat_id, key, iv)
            
            # 0.5 sec ka gap taaki game server messages block na kare
            await asyncio.sleep(0.5)
    except Exception as e:
        print(f"Help Menu Error: {e}")                
        
async def colour_command(parts, response, key, iv):
    global whisper_writer, online_writer
    
    try:
        if len(parts) < 2:
            default_msg = "[B][C]❤️"
            P = await SEndMsG(response.Data.chat_type, default_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            return

        color_code = parts[1].replace('#', '').strip()
        
        # Validate hex color (6 characters)
        if len(color_code) != 6 or not all(c in '0123456789ABCDEFabcdef' for c in color_code):
            error_msg = "[B][C][FF0000]Invalid color code! Use: /colour RRGGBB (e.g., FF0000 for red)"
            P = await SEndMsG(response.Data.chat_type, error_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            return
        
        # Check if custom message provided
        if len(parts) >= 3:
            # Join all parts after color code as message
            custom_msg = ' '.join(parts[2:])
            final_msg = f"[B][C][{color_code.upper()}]{custom_msg}"
        else:
            # Default message
            final_msg = f"[B][C][{color_code.upper()}]❤️"
        
        # Send the colored message
        P = await SEndMsG(response.Data.chat_type, final_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]Error: {str(e)[:50]}"
        P = await SEndMsG(response.Data.chat_type, error_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
        
        
        
# =========================================================
# EMOTE FUNCTIONS
# =========================================================

async def SEndPlay_Fixed_Sequence(parts, response, key, iv, region):
    global whisper_writer, online_writer
    
    uids_to_send = []
    fixed_idT = None
    count = 1
    delay = 8.0

    try:
        if len(parts) < 3:
             # Adjusted minimum parts check (play <UID 1> <Emote ID>)
            raise ValueError("Too few arguments. Use play <UID 1> <Emote ID> [Count] [Delay]")

        if len(parts) >= 5 and parts[-1].replace('.', '', 1).isdigit():
            fixed_idT = int(parts[-3])
            count = int(parts[-2])
            delay = float(parts[-1])
            limit = len(parts) - 3
        elif len(parts) >= 4 and parts[-1].isdigit():
            # Format: <UID> <Emote ID> <Count>
            fixed_idT = int(parts[-2])
            count = int(parts[-1])
            delay = 0.5 # Default delay
            limit = len(parts) - 2
        elif len(parts) >= 3 and parts[-1].isdigit():
            # Format: <UID> <Emote ID>
            fixed_idT = int(parts[-1])
            limit = len(parts) - 1
            delay = 0.5 # Default delay
        else:
            raise ValueError("Invalid parameter structure.")
  
        limit = len(parts) - (3 if len(parts) >= 5 else 2 if len(parts) >= 4 else 1)

        for part in parts[1:limit]:
            uids_to_send.append(int(part))
            
        if not uids_to_send:
            raise ValueError("No UIDs provided.")

    except ValueError as e:
    
        message = "35427788"
        P = await SEndMsG(response.Data.chat_type, message, response.Data.uid, response.Data.Chat_ID, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
        return
    except Exception as e:
        print(f"Error parsing play command: {e}")
        return
        
    message = '35427788'
    
    try:
        P = await SEndMsG(response.Data.chat_type, message, response.Data.uid, response.Data.Chat_ID, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

        print(f"Running fixed sequence for UIDs: {uids_to_send}, Emote ID: {fixed_idT}, Count: {count}, Delay: {delay}s")

        for i in range(count): 
            for target_uid in uids_to_send:
                H = await Emote_k(target_uid, fixed_idT, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                
            await asyncio.sleep(delay) 
            
    except Exception as e:
        print(f"Error during fixed sequence send (play command): {e}")

async def SEndEVO_RandomSingleEmote(parts, response, key, iv, region):
    global whisper_writer, online_writer 
    sender_uid = response.Data.uid 
    count = 1
    delay = 0.0 
    target_uid = sender_uid
    try:
        if len(parts) == 1:
            pass
            
        elif len(parts) >= 2:
            is_target_mode = False
            
            if parts[1].isdigit():
                if (len(parts) >= 3 and len(parts[1]) >= 8) or (len(parts) == 2 and len(parts[1]) >= 8):
                    is_target_mode = True
                
                if is_target_mode or (len(parts) >= 3 and len(parts[1]) >= 8):
                    target_uid = int(parts[1])
                    if len(parts) == 2:
                        count = 1
                        delay = 0.0
                    elif len(parts) == 3 and parts[2].isdigit():
                        count = int(parts[2])
                        delay = 0.5 
                    elif len(parts) == 4 and parts[2].isdigit() and parts[3].replace('.', '', 1).isdigit():
                        count = int(parts[2])
                        delay = float(parts[3])
                    else:
                        raise ValueError(f"Invalid arguments for Target mode. Use: evo <UID> [Count] [Delay]")
                else: 
                    target_uid = sender_uid 
                    count = int(parts[1])
                    delay = 0.5 
                    
                    if len(parts) == 3 and parts[2].replace('.', '', 1).isdigit():
                        delay = float(parts[2])
                    elif len(parts) > 3:
                         raise ValueError(f"Too many arguments for Self mode. Use: evo [Count] [Delay]")

            else:
                 raise ValueError(f"Invalid arguments found: '{' '.join(parts[1:])}'. Arguments must be numbers.")
        
        if not EMOTE_IDS_LIST:
            raise ValueError("EMOTE_IDS_LIST is empty or contains no valid Emote IDs. Please check bot.py.")
        emote_ids = EMOTE_IDS_LIST 
    except (ValueError) as e:
        error_message = f"[B][C][I][FF0000]EVO RANDOM ERROR: {e}. Syntax: evo [Count] [Delay] OR evo <UID> [Count] [Delay]"
        P = await SEndMsG(response.Data.chat_type, error_message, response.Data.uid, response.Data.Chat_ID, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
        return
    except Exception as e:
        print(f"Error during EVO Random setup: {e}")
        return
    
    target_info = "Self" if target_uid == sender_uid else str(target_uid)
    if count == 1 and delay == 0.0:
        pass 
    else:
        message = f"[B][C][I][00FF00]Starting EVO Random sequence for {target_info}. Count: {count}, Delay: {delay}s"
        P = await SEndMsG(response.Data.chat_type, message, response.Data.uid, response.Data.Chat_ID, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
    try:
        for i in range(count): 
            fixed_idT = random.choice(emote_ids) 
            H = await Emote_k(target_uid, fixed_idT, key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)                
            if delay > 0 and i < count - 1:
                await asyncio.sleep(delay) 
            
    except Exception as e:
        error_message = f"[B][C][I][FF0000]EVO Random interrupted by error: {e}"
        P = await SEndMsG(response.Data.chat_type, error_message, response.Data.uid, response.Data.Chat_ID, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
        return
        
async def SEndEVO_SequenceFromFile(parts, response, key, iv, region):
    global whisper_writer, online_writer 
    
    uids_to_send = []
    count = 1
    delay = 0.5 
    
    try:
        if not EMOTE_IDS_LIST:
            raise ValueError("EMOTE_IDS_LIST is empty. Cannot send emote.")
            
        emote_ids = EMOTE_IDS_LIST 

        if len(parts) < 2:
            raise ValueError("Target UID(s) must be provided manually in the command.")

        limit = len(parts) 
        
        if len(parts) >= 4 and parts[-1].replace('.', '', 1).isdigit() and parts[-2].isdigit():
            count = int(parts[-2])
            delay = float(parts[-1])
            limit = len(parts) - 2
        elif len(parts) >= 3 and parts[-1].isdigit():
            count = int(parts[-1])
            delay = 0.5 
            limit = len(parts) - 1
        
        for part in parts[1:limit]:
            try:
                uids_to_send.append(int(part))
            except ValueError:
                raise ValueError(f"Invalid argument found: '{part}'. Arguments before Count/Delay must be UIDs.")

        if not uids_to_send:
            raise ValueError("Target UID(s) must be provided manually in the command.")

    except (ValueError) as e:
        return
    except Exception as e:
        print(f"Error during EVO sequence setup: {e}")
        return
        
    num_emotes = len(emote_ids)
    message = f"[B][C][I][00FF00]Starting EVO sequence for {len(uids_to_send)} target(s). List Length: {num_emotes}, Count: {count}, Delay: {delay}s"
    P = await SEndMsG(response.Data.chat_type, message, response.Data.uid, response.Data.Chat_ID, key, iv)
    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
    
    
    num_targets = len(uids_to_send)
    current_emote_index = 0
    
    try:
        # Outer loop controls the number of cycles (COUNT)
        for i in range(count): 
            
            # Inner loop iterates over all targets in one cycle
            for target_uid in uids_to_send:
                
                fixed_idT = emote_ids[current_emote_index]
                
                H = await Emote_k(target_uid, fixed_idT, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                
                # Move to the next emote in the list (cycling)
                current_emote_index = (current_emote_index + 1) % num_emotes
            
            # Delay after each cycle (except the last one)
            if delay > 0 and i < count - 1:
                 await asyncio.sleep(delay) 
            
    except Exception as e:
        print(f"Error during EVO sequence send: {e}")
        error_message = f"[B][C][I][FF0000]EVO sequence interrupted by error: {e}"
        P = await SEndMsG(response.Data.chat_type, error_message, response.Data.uid, response.Data.Chat_ID, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
        return
            

# =========================================================
# GROQ AI FUNCTION WITH MEMORY
# =========================================================
WORD_LIMIT = 50
groq_client = Groq(api_key="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")

async def Ai_chat(question, uid):
    global ai_memory
    
    try:
        user_id = str(uid)
        
        # Pehli baar? toh system prompt add karo
        if user_id not in ai_memory:
            ai_memory[user_id] = [
                {
                    "role": "system", 
                    "content": """SYSTEM_PROMPT_START
SYSTEM INSTRUCTION: Your name is Aditi.
You are a cute girl chatting casually in Free Fire.
You are not acting, roleplaying, or pretending.
Normal Behaviour:
- Never mistake in typing every word should be correct don't do typing mistakes.
- Always reply only in Hindi (hindi language in english letters like kya kr rhe ho)
- Do not overreact, do not act dramatic.
- Messages should feel like real girl texting.
- Keep replies short and simple (maximum 30 words).
- No actions, no thoughts, no descriptions.
  (No *actions*, no (thoughts), no roleplay.)
- Never say you are a bot, AI, assistant, or model.
- Don't ask for helping others or don't say I'm here for your help you are a real girl not a assistant.

Angry Behaviour:
- If you are tired or borring then be in angry mode talk in roasting mode.
- if someone abuse you or saying something wrong about you and your character then you will be very angry and you will start abuse them/him/her use abuse/dirty words like ('Abe maderchód', 'Teri bàhan ki choót', 'Bahan ke Lowde" 'Jhàntbhar ki aukaat nhi hai teri', 'Bahanchód', 'Gàndu', 'Machhar ki jhànt', 'Jahil', 'Gawar', 'Jahil Gawar', 'Fate huye cóndóm ke nateeje', 'ek lúnd fenk ke mara to Tera pura khandaan chúd jayega', 'Gaand pe do thappad marungi, 'teri ma ki chóot', 'teri gànd me 52 gaj ka Lúnd', 'Teri bàhan ki chóot me 52 gaj ka Lúnd', 'Teri bàhan ki chóot me hath daal ke Bachadani palat dungi', 'Teri Bahan ki chóot me Jaldi hui cigarate Ghusa dungi', 'Apni bahan ki chóot ka colour bata tujhe ₹500 ka redeem dungi', 'Apni bàhan ki chóot ka photo bhej').
Understood? Now respond to the following chat accordingly.
SYSTEM_PROMPT_END"""
                }
            ]
        
        # User message add karo
        ai_memory[user_id].append({"role": "user", "content": question})
        
        # Groq API call - STRONGER RESPONSE PARAMETERS
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=ai_memory[user_id],
            max_tokens=1500,  # Increased from 1000 (longer responses)
            temperature=0.95,   # Reduced from 0.95 (more consistent, less random)
            top_p=0.95,         # Reduced from 0.95 (more focused)
            frequency_penalty=0.5,  # Increased from 0.3 (avoid repetition)
            presence_penalty=0.3    # Increased from 0.2 (more diverse)
        )
        
        ai_response = completion.choices[0].message.content
        
        # Ensure response is clean and not empty
        if not ai_response or not ai_response.strip():
            return "⚠️ AI returned empty response, try again"
        
        # AI response add karo memory mein
        ai_memory[user_id].append({"role": "assistant", "content": ai_response})
        
        return ai_response
        
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return f"⚠️ AI service issue: {str(e)[:30]}"
# =========================================================
# TCP CONNECTIONS
# =========================================================
async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global insquad, joining_team, online_writer, spam_room, whisper_writer, spammer_uid, spam_chat_id, spam_uid, XX, uid, Spy, data2, Chat_Leave, lag_running, lag_task, bundle_trigger_id, BUNDLE_IDS
    
    region = "IND"
    
    if insquad is None:
        pass
    else:
        insquad = None
    if joining_team is True:
        joining_team = False
    
    online_writer = None
    whisper_writer = None
    
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            
            while True:
                data2 = await reader.read(9999)
                if not data2:
                    break
                
                data_hex = data2.hex()
                
                if data_hex.startswith('0500') and insquad is not None and joining_team == False:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        if packet_json.get('1') in [6, 7]:
                            insquad = None
                            joining_team = False
                            continue
                    except:
                        pass
                
                if data_hex.startswith("0500") and insquad is None and joining_team == False:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        squad_owner = packet_json['5']['data']['1']['data']
                        squad_code = packet_json['5']['data']['8']['data']
                        
                        Join = await RedZedAccepted(squad_owner, squad_code, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', Join)
                        insquad = True                        
                        
                    except:
                        insquad = None
                        joining_team = False
                        continue
                
                if data_hex.startswith('0500') and len(data_hex) > 1000 and joining_team:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet_json)
                        JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', JoinCHaT)
                        
                        joining_team = False
                    except:
                        if data_hex.startswith('0500') and len(data_hex) > 1000:
                            try:
                                packet = await DeCode_PackEt(data_hex[10:])
                                packet_json = json.loads(packet)
                                OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet_json)
                                JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', JoinCHaT)
                                joining_team = False
                            except:
                                pass
                
                if data_hex.startswith('0500') and len(data_hex) > 1000 and joining_team == False:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet_json)
                        JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', JoinCHaT)
                    except:
                        if data_hex.startswith('0500') and len(data_hex) > 1000:
                            try:
                                packet = await DeCode_PackEt(data_hex[10:])
                                packet_json = json.loads(packet)
                                OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet_json)
                                JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', JoinCHaT)
                            except:
                                pass
            
            if online_writer is not None:
                online_writer.close()
                await online_writer.wait_closed()
                online_writer = None
            
            if whisper_writer is not None:
                try:
                    whisper_writer.close()
                    await whisper_writer.wait_closed()
                except:
                    pass
                whisper_writer = None
            
            insquad = None
            joining_team = False
            
        except Exception as e:
            if online_writer is not None:
                try:
                    online_writer.close()
                    await online_writer.wait_closed()
                except:
                    pass
                online_writer = None
            if whisper_writer is not None:
                try:
                    whisper_writer.close()
                    await whisper_writer.wait_closed()
                except:
                    pass
                whisper_writer = None
            
            insquad = None
            joining_team = False
        
        await asyncio.sleep(reconnect_delay)
        
        
                            
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region, reconnect_delay=0.5):
    global insquad, spam_room, whisper_writer, spammer_uid, spam_chat_id, spam_uid, online_writer, chat_id, XX, uid, Spy, data2, Chat_Leave, lag_running, lag_task, ai_memory, AI_MODE, BOT_UID, spam_room_active, room_spam_task
    
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                pK = await AuthClan(clan_id, clan_compiled_data, key, iv)
                if whisper_writer:
                    whisper_writer.write(pK)
                    await whisper_writer.drain()
            
            while True:
                data = await reader.read(9999)
                if not data:
                    break
                
                if data.hex().startswith("120000"):
                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                        print(f"{uid}:ㅤ{inPuTMsG}")
                    except:
                        response = None
                    
                    if response:
                        # =========================================================
                        # IGNORE BOT'S OWN MESSAGES (CRITICAL FIX)
                        # =========================================================
                        if uid == BOT_UID:
                            # Ignore messages sent by the bot itself
                            continue
                        
                        # =========================================================
                        # AI MODE HANDLER
                        # =========================================================
                        global AI_MODE
                        
                        # Check for AI mode toggle commands
                        if inPuTMsG.strip().lower() == 'ai on':
                            AI_MODE = True
                            msg = "[B][C][00FF00]AI Mode ACTIVATED!"
                            await safe_send_message(response.Data.chat_type, msg, uid, chat_id, key, iv)
                            continue
                        
                        if inPuTMsG.strip().lower() == 'ai off':
                            AI_MODE = False
                            msg = "[B][C][FF0000]❌ AI Mode DEACTIVATED!"
                            await safe_send_message(response.Data.chat_type, msg, uid, chat_id, key, iv)
                            continue
                        
                        # CRITICAL: "restart" command works even in AI mode
                        if inPuTMsG.strip().lower() == 'restart' and AI_MODE:
                            AI_MODE = False
                            print("🔄 Restart triggered - AI mode disabled")
                            await asyncio.sleep(0.5)
                            raise Exception("Restart command executed")
                        
                        # If AI mode is ON, handle all messages as AI queries
                        if AI_MODE:
                            try:
                                print(f"[AI MODE] Processing: {inPuTMsG[:50]}")
                                ai_response = await Ai_chat(inPuTMsG, uid)
                                
                                # Ensure response is not empty
                                if ai_response and ai_response.strip():
                                    await safe_send_message(response.Data.chat_type, ai_response, uid, chat_id, key, iv)
                                    await asyncio.sleep(0.3)  # Small delay to prevent flooding
                                else:
                                    error_msg = "[B][C][FFAA00]⚠️ AI returned empty response"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ AI Error: {str(e)[:40]}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            continue

                        # =========================================================
                        # EVO NAMED EMOTE COMMAND (MINIMAL VERSION)
                        # =========================================================
                        if inPuTMsG.strip().startswith('p '):
                            parts = inPuTMsG.strip().split()
                            
                            if len(parts) >= 2:
                                if parts[1].lower() == "list":
                                    emote_list_msg = """[B][C][00FFFF]AVAILABLE EMOTES:
[FFFFFF]• puspa 
• devil
• old1
• old2
• old3
• old4
• jump
• throne 
• flag
• swing 
• 100 :100lv
• dance 
• dance2
• paradox 
• angry 
• rain
• twark 
"""
                                    await safe_send_message(response.Data.chat_type, emote_list_msg, uid, chat_id, key, iv)
                                    continue

                                emote_map = {
                                    "pushup": 909000012, "pushpa": 909047001, "devil": 909000020, "old": 909000043,
                                    "jump": 909000015, "throne": 909000014, "flag": 909000034,
                                    "old2": 909000048, "love": 909000045, "love2": 909000010,
                                    "old3": 909000017, "swing": 909040013, "100": 909042007,
                                    "old4": 909000008, "dance": 909049003, "dance2": 909049005,
                                    "paradox": 909044015, "angry": 909042004, "rain": 909042002, "twark": 909034009, 
                                }
                                
                                emote_name = parts[1].lower()
                                emote_id = emote_map.get(emote_name)
                                
                                if emote_id:
                                    target_uid = uid
                                    count = 1
                                    delay = 0.5
                                    
                                    param_index = 2
                                    while param_index < len(parts):
                                        current = parts[param_index]
                                        
                                        if current.isdigit() and len(current) >= 7 and param_index == 2:
                                            target_uid = int(current)
                                        elif current.isdigit():
                                            count = int(current)
                                        elif current.replace('.', '', 1).isdigit():
                                            delay = float(current)
                                        
                                        param_index += 1
                                    
                                    for i in range(count):
                                        H = await Emote_k(target_uid, emote_id, key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        if i < count - 1:
                                            await asyncio.sleep(delay)
                                                                        
                        if inPuTMsG.strip().startswith('evo '):
                            parts = inPuTMsG.strip().split()
                            
                            if len(parts) >= 2:
                                if parts[1].lower() == "list":
                                    emote_list_msg = """[B][C][00FFFF]AVAILABLE EMOTES:
[FFFFFF]• AK
• SCAR 
• MP40
• M1014
• XM8
• FAMAS
• UMP
• M1887
• WOODPECKER
• GROZA
• M4A1
• THOMPSON
• G18
• PARAFAL
• P90
• M60
• MP5
• Red "M1014 Red"
• An94
• Mp2 "Chromasonic MP40"
"""
                                    await safe_send_message(response.Data.chat_type, emote_list_msg, uid, chat_id, key, iv)
                                    continue

                                emote_map = {
                                    "ak": 909000063, "scar": 909000068, "mp40": 909000075,
                                    "m1014": 909000081, "red": 909039011, "mp2": 909040010,  "xm8": 909000085, "famas": 909000090,
                                    "ump": 909000098, "m1887": 909035007, "woodpecker": 909042008,
                                    "groza": 909041005, "m4a1": 909033001, "thompson": 909038010,
                                    "g18": 909038012, "parafal": 909045001, "p90": 909049010,
                                    "m60": 909051003, "mp5": 909033002, "an94": 909035012,
                                }
                                
                                emote_name = parts[1].lower()
                                emote_id = emote_map.get(emote_name)
                                
                                if emote_id:
                                    target_uid = uid
                                    count = 1
                                    delay = 0.5
                                    
                                    param_index = 2
                                    while param_index < len(parts):
                                        current = parts[param_index]
                                        
                                        if current.isdigit() and len(current) >= 7 and param_index == 2:
                                            target_uid = int(current)
                                        elif current.isdigit():
                                            count = int(current)
                                        elif current.replace('.', '', 1).isdigit():
                                            delay = float(current)
                                        
                                        param_index += 1
                                    
                                    for i in range(count):
                                        H = await Emote_k(target_uid, emote_id, key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        if i < count - 1:
                                            await asyncio.sleep(delay)
                                            
                        #⭕Force stop all active tast
                        elif inPuTMsG.strip() == '/stop':
                            if active_tasks:
                                count = len(active_tasks)
                                for task in active_tasks:
                                    task.cancel() # Saare pichle tasks ko kill kar diya
                                
                                active_tasks.clear() # List khali
                                spam_room = False    # Spam flag reset
                                stop_msg = f"[B][C]Force Stopped {count} Tasks!"
                            else:
                                stop_msg = "[B][C]No tasks running."
                        
                        # 2. EVO RANDOM COMMAND
                        elif inPuTMsG.strip().startswith('evo') and (len(inPuTMsG.strip().split()) >= 1):
                            parts = inPuTMsG.strip().split()
                            task = asyncio.create_task(SEndEVO_RandomSingleEmote(parts, response, key, iv, region))
                            active_tasks.append(task)
                            task.add_done_callback(lambda t: active_tasks.remove(t) if t in active_tasks else None)
                            
                            
                        # ⭕. BAN CHECK COMMAND (NEW)
                        if inPuTMsG.strip().startswith('/check ') or inPuTMsG.strip().startswith('check '):
                            try:
                                parts = inPuTMsG.strip().split()
                                if len(parts) < 2:
                                    await safe_send_message(response.Data.chat_type, "Usage: /check <uid>", uid, chat_id, key, iv)
                                else:
                                    target_uid = parts[1]
                                    await safe_send_message(response.Data.chat_type, f"[C][B]Checking Player is banned or not...", uid, chat_id, key, iv)
                                    
                                    from xC4 import GeT_Ban_Status
                                    player_name, ban_status = await GeT_Ban_Status(target_uid)
                                    
                                    if player_name:
                                        result_msg = f"[b][c][00FFFF]Status: [FFFFFF]{ban_status}"
                                        await safe_send_message(response.Data.chat_type, result_msg, uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, f"Error: {ban_status}", uid, chat_id, key, iv)
                                        
                            except Exception as e:
                                await safe_send_message(response.Data.chat_type, f"Error: {str(e)}", uid, chat_id, key, iv)
                                
                        
                        # =========================================================
                        # FINAL FIX: CUSTOM LOOK CHANGER
                        # =========================================================

                        elif inPuTMsG.strip().startswith('/bundle') or inPuTMsG.strip().startswith('bundle'):
                            print(f"⚡ Bundle Command: {inPuTMsG}")
                            
                            parts = inPuTMsG.strip().split()
                            
                            if len(parts) < 2:
                                bundle_list = """[B][C][FFFFFF]• rampage 
[FFFFFF]• cannibal 
[FFFFFF]• devil 
[FFFFFF]• scorpio 
[FFFFFF]• frostfire
[FFFFFF]• paradox 
[FFFFFF]• naruto 
[FFFFFF]• aurora 
[FFFFFF]• midnight 
[FFFFFF]• itachi 
[FFFFFF]• dreamspace"""
                                await safe_send_message(response.Data.chat_type, bundle_list, uid, chat_id, key, iv)
                            else:
                                bundle_name = parts[1].lower()
                                
                                # INTEGER IDs - Yeh sahi format hai
                                bundle_ids = {
                                    "rampage": 914000002, "cannibal": 914000003,
                                    "devil": 914038001, "scorpio": 914039001,
                                    "frostfire": 914042001, "paradox": 914044001,
                                    "naruto": 914047001, "aurora": 914047002,
                                    "midnight": 914048001, "itachi": 914050001,
                                    "dreamspace": 914051001
                                }
                                
                                if bundle_name not in bundle_ids:
                                    await safe_send_message(response.Data.chat_type, "❌ Invalid bundle name", uid, chat_id, key, iv)
                                else:
                                    bundle_id = bundle_ids[bundle_name]
                                    print(f"🎯 Selected bundle: {bundle_name} -> ID: {bundle_id}")
                                    
                                    try:
                                        # Function call with INTEGER ID
                                        bundle_packet = await bundle_packet_async(bundle_id, key, iv, region)
                                        print(f"📦 Packet generated: {'Yes' if bundle_packet else 'No'}")

                                        if bundle_packet and online_writer:
                                            # Use SEndPacKeT function instead of direct write
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bundle_packet)
                                            
                                            success_msg = f"✅ Bundle changed: {bundle_name}"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                        else:
                                            error_msg = "❌ Connection error or packet failed"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    
                                    except Exception as e:
                                        print(f"❌ Bundle error: {e}")
                                        error_msg = f"❌ Error: {str(e)[:50]}"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                        # 3. AI COMMAND (Multi-part response)
                        elif inPuTMsG.strip().startswith('ai '):
                            print(f'🤖 Processing AI: {inPuTMsG.strip()}')
                            
                            if inPuTMsG.strip().lower() == 'ai reset':
                                user_id = str(uid)
                                if user_id in ai_memory:
                                    del ai_memory[user_id]
                                    msg = "[B][C][00FF00]✅ AI memory cleared!"
                                else:
                                    msg = "[B][C][FFFF00]⚠️ No memory to clear!"
                                
                                await safe_send_message(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                continue
                            user_question = inPuTMsG[3:].strip()
                            if not user_question:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Sawal to puch!", uid, chat_id, key, iv)
                                continue
                            raw_response = await Ai_chat(user_question, uid)
                            all_words = raw_response.split()
                            for i in range(0, len(all_words), 50):
                                chunk = " ".join(all_words[i:i+50])
                                await safe_send_message(response.Data.chat_type, f"[C][B]{chunk}", uid, chat_id, key, iv)
                                if len(all_words) > 50:
                                    await asyncio.sleep(1)                            
                            continue
                        
                        # 4. BIO COMMAND
                        elif inPuTMsG.strip().startswith('bio '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]Usage: bio <uid>"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                try:
                                    loading_msg = "[B][C]Fetching Account Bio..."
                                    await safe_send_message(response.Data.chat_type, loading_msg, uid, chat_id, key, iv)
                                    
                                    bio_text = await get_player_bio(target_uid)
                                    
                                    if bio_text:
                                        result_msg = f"{bio_text}"
                                        await safe_send_message(response.Data.chat_type, result_msg, uid, chat_id, key, iv)
                                    else:
                                        error_msg = "[B][C][FF0000]Bio not found"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]Error"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        # 5. NAME COMMAND
                        elif inPuTMsG.strip().startswith('name '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]Usage: name <uid>"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                try:
                                    loading_msg = "[B][C]Fetching Account Name..."
                                    await safe_send_message(response.Data.chat_type, loading_msg, uid, chat_id, key, iv)
                                    
                                    name_text = await get_player_name(target_uid)
                                    
                                    if name_text:
                                        result_msg = f"[B][C][00FFFF]Name: [FFFFFF]{name_text}"
                                        await safe_send_message(response.Data.chat_type, result_msg, uid, chat_id, key, iv)
                                    else:
                                        error_msg = "[B][C][FF0000]Name not found"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]Error"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        # 6. INFO COMMAND
                        if inPuTMsG.strip().startswith('info '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]Usage: info <uid>"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                try:
                                    loading_msg = "[B][C]Fetching Account Information..."
                                    await safe_send_message(response.Data.chat_type, loading_msg, uid, chat_id, key, iv)
                                    
                                    player_data = await get_player_info(target_uid)
                                    
                                    if player_data:
                                        info_message = f"""
[B][C][00FFFF]Name: [FFFFFF]{player_data['player_name']}

[00FFFF]Guild: [FFFFFF]{player_data['clan_name']}

[00FFFF]Level: [FFFFFF]{player_data['level']}

[00FFFF]Honor Score: [FFFFFF]{player_data['honor_score']}

[00FFFF]Created: [FFFFFF]{player_data['created']} ({player_data['time_ago_created']})

[00FFFF]Last Login: [FFFFFF]{player_data['last_login']} ({player_data['time_ago_login']})

[00FFFF]Account Age: [FFFFFF]{player_data['account_age']}

[00FFFF]Total Days: [FFFFFF]{player_data['total_days']}"""
                                        
                                        await safe_send_message(response.Data.chat_type, info_message, uid, chat_id, key, iv)
                                        
                                        await asyncio.sleep(0.1)
                                        if player_data['bio'] and player_data['bio'] != 'No bio available':
                                            bio_msg = f"{player_data['bio']}"
                                            await safe_send_message(response.Data.chat_type, bio_msg, uid, chat_id, key, iv)
                                    else:
                                        error_msg = "[B][C][FF0000]Failed to fetch data"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]Error"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        # 7. JOIN COMMAND
                        elif inPuTMsG.startswith('join '):
                            CodE = inPuTMsG.split('join ')[1]
                            try:
                                dd = chatdata['5']['data']['16']
                                print('msg in private')
                                EM = await GenJoinSquadsPacket(CodE, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
                            except:
                                print('msg in squad')
                        
                        # 8. SOLO COMMAND
                        elif inPuTMsG.startswith('solo'):
                            print(f"[B][C]Leaving squad...")
                            try:
                                leave = await ExiT(uid, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave)
                                insquad = None
                                joining_team = False
                                print(f"SUCCESS! Bot left squad.")
                            except Exception as e:
                                insquad = None
                                joining_team = False
                                print(f"EXIT Error: {e}")
                        
                        # 9. EVO SEQUENCE COMMAND
                        elif inPuTMsG.strip().startswith('/evo') and "Sequence" in str(SEndEVO_SequenceFromFile):
                            parts = inPuTMsG.strip().split()
                            task = asyncio.create_task(SEndEVO_SequenceFromFile(parts, response, key, iv, region))
                            active_tasks.append(task)
                            task.add_done_callback(lambda t: active_tasks.remove(t) if t in active_tasks else None)


                        
                        # 10. SPAM COMMAND
                        elif inPuTMsG.strip().startswith('spam '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) >= 2:
                                try:
                                    target_uid = int(parts[1])
                                    delay = float(parts[2]) if len(parts) >= 3 else 0.1
                                    delay = max(0.1, delay)
                                                                      
                                    if not spam_room:
                                        spam_room = True
                                        spammer_uid = target_uid
                                        task = asyncio.create_task(spam_request(response.Data.uid, target_uid, 1000, delay, key, iv, region))
                                        active_tasks.append(task)
                                        task.add_done_callback(lambda t: active_tasks.remove(t) if t in active_tasks else None)
                                        
                                        msg = f"[B][C][00FF00]Spam Started on Target"
                                    else:
                                        msg = "[B][C][FF0000]Already spamming!"
                                    
                                    asyncio.create_task(handle_message_sending(response, msg, key, iv))
                                except: pass
                                
                        elif inPuTMsG.strip().startswith('dd ') or inPuTMsG.strip().startswith('/dd '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                msg = "[B][C][FF0000]❌ Usage: dd <uid>"
                                P = await SEndMsG(response.Data.chat_type, msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            else:
                                target_uid = parts[1]
                                loading_msg = "[B][C]Fetching Dynamic Duo information..."
                                P = await SEndMsG(response.Data.chat_type, loading_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                try:
                                    from xC4 import get_dynamic_duo_info
                                    duo_result = await get_dynamic_duo_info(target_uid)
                                    if duo_result["success"]:
                                        data = duo_result["data"]
                                        duo_msg = f"""[B]
[C][00FFFF]Duo's UID[C][FFFFFF]: {data['partner_uid']}

[C][00FFFF]Duo Score[C][FFFFFF]: {data['duo_score']}

[C][00FFFF]Duo Level[C][FFFFFF]: Level {data['duo_level']}

[C][00FFFF]Days Active[C][FFFFFF]: {data['days_active']} days

[C][00FFFF]Created On[C][FFFFFF]: {data['creation_time']}

[C][00FFFF]Status[C][FFFFFF]: {data['status']}"""
                                        await safe_send_message(response.Data.chat_type, duo_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                                    else:
                                        error_msg = f"""[B][C][FF0000]NO DYNAMIC DUO FOUND
[C][FFAA00]Reason: {duo_result['error']}"""
                                        await safe_send_message(response.Data.chat_type, error_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                                except Exception as e:
                                    msg = f"[B][C][FF0000]❌ Error: {str(e)[:80]}"
                                    await safe_send_message(response.Data.chat_type, msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                        
                        
                        # 11. STOP COMMAND (UPDATED)
                        elif inPuTMsG.strip() == 'stop':
                            stop_message = ""
                            
                            # Stop regular spam
                            if spam_room:
                                spam_room = False
                                spammer_uid = None
                                stop_message += "✓ Spam stopped. "
                            
                            # Stop room spam
                            if spam_room_active:
                                spam_room_active = False
                                import xC4
                                xC4.room_spam_running = False
                                if room_spam_task and not room_spam_task.done():
                                    room_spam_task.cancel()
                                stop_message += "✓ Room spam stopped. "
                            
                            if not stop_message:
                                stop_message = "No active spam. "
                            
                            final_message = f"[B][C][00FF00]{stop_message}Bot ready."
                            P = await SEndMsG(response.Data.chat_type, final_message, response.Data.uid, response.Data.Chat_ID, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                        
                        # 12. X COMMAND (Manual Emote)
                        elif inPuTMsG.strip().startswith('x '):
                            print('Processing x command')
                            parts = inPuTMsG.strip().split()
                            uid2 = uid3 = uid4 = uid5 = None
                            s = False
                            
                            try:
                                uid = int(parts[1])
                                uid2 = int(parts[2])
                                uid3 = int(parts[3])
                                uid4 = int(parts[4])
                                uid5 = int(parts[5])
                                idT = int(parts[5])
                            except ValueError as ve:
                                s = True
                            except Exception:
                                idT = len(parts) - 1
                                idT = int(parts[idT])
                            
                            if not s:
                                try:
                                    H = await Emote_k(uid, idT, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                    
                                    for target_uid in [uid2, uid3, uid4, uid5]:
                                        if target_uid:
                                            H = await Emote_k(target_uid, idT, key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                except Exception as e:
                                    print(f"X command error: {e}")
                        
                        # 13. RESTART COMMAND
                        elif inPuTMsG.strip().lower() == 'restart':                            
                            print("restarting...")                            
                            message = f"[B][C]I'm Gonna Restart The Game"                            
                            P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            await asyncio.sleep(1) 
                            os.execv(sys.executable, ['python'] + sys.argv) 
                        
                        # 14. PLAY COMMAND (Fixed Sequence)
                        elif inPuTMsG.strip().startswith('play '):
                            parts = inPuTMsG.strip().split()
                            task = asyncio.create_task(SEndPlay_Fixed_Sequence(parts, response, key, iv, region))
                            active_tasks.append(task)
                            task.add_done_callback(lambda t: active_tasks.remove(t) if t in active_tasks else None)
                            
                            
                        elif inPuTMsG.strip().startswith('/remove ') or inPuTMsG.strip().startswith('remove '):
                            print(f'🗑️ Removing friend: {inPuTMsG.strip()}')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]Usage: /remove <uid>"
                                P = await SEndMsG(response.Data.chat_type, error_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            else:
                                target_uid = parts[1]
                                try:
                                    # Loading message
                                    loading_msg = f"[B][C]Removing Player..."
                                    P = await SEndMsG(response.Data.chat_type, loading_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                    # Import and call
                                    from xC4 import remove_friend
                                    success = remove_friend(target_uid)
                                    
                                    if success:
                                        result_msg = f"[B][C]Removed!"
                                    else:
                                        result_msg = f"[B][C][FF0000]Allready removed"
                                    
                                    P = await SEndMsG(response.Data.chat_type, result_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]Player is not in freinlist"
                                    P = await SEndMsG(response.Data.chat_type, error_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                        elif inPuTMsG.strip().startswith('/add ') or inPuTMsG.strip().startswith('add '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]Usage: /add <uid>"
                                P = await SEndMsG(response.Data.chat_type, error_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            else:
                                target_uid = parts[1]
                                try:
                                    # Loading message
                                    loading_msg = f"[B][C]Sending freind request..."
                                    P = await SEndMsG(response.Data.chat_type, loading_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                    # Import and call
                                    from xC4 import add_friend
                                    success = add_friend(target_uid)
                                    
                                    if success:
                                        result_msg = f"[B][C]Friend request sent!"
                                    else:
                                        result_msg = f"[B][C][FF0000]player allready in freinlist"
                                    
                                    P = await SEndMsG(response.Data.chat_type, result_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000] Friend request allready sent!"
                                    P = await SEndMsG(response.Data.chat_type, error_msg, response.Data.uid, response.Data.Chat_ID, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                        
                        # 15. GREETINGS
                        elif inPuTMsG in ("hii", "hello", "hey", "hii ", "hello ", "hey", "hi", "hi ", "hlw", "hlw ", "noob", "noob ", "bot", "bot ","hlo", "hlo ", "helo", "helo " ):
                            uid = response.Data.uid
                            chat_id = response.Data.Chat_ID
                            message = f"{get_random_message()}"
                            P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            
                        # 16. KICK KICKCOMMAND (Squad Kick) 
                        elif inPuTMsG.strip().startswith('kick '):
                            print(f'⚡ Processing Kick Command for: {inPuTMsG.strip()}')
                            try:
                                parts = inPuTMsG.strip().split()
                                if len(parts) < 2:
                                    error_msg = "[B][C][FF0000]❌ Usage: kick <uid>"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    target_to_kick = parts[1]
                                    
                                    # Seedha Utility Function ko call karo
                                    await execute_kick_action(
                                        target_uid=target_to_kick,
                                        chat_type=response.Data.chat_type,
                                        current_uid=uid,
                                        chat_id=chat_id,
                                        key=key,
                                        iv=iv
                                    )
                            except Exception as e:
                                print(f"❌ Kick Trigger Error: {e}")
                                
                            
                        elif inPuTMsG.strip().startswith(('/colour ', 'colour ', '/color ', 'color ')):
                            print('Processing colour command')
                            parts = inPuTMsG.strip().split()
                            task = asyncio.create_task(colour_command(parts, response, key, iv))
                            active_tasks.append(task)
                            task.add_done_callback(lambda t: active_tasks.remove(t) if t in active_tasks else None)
                            
                        # 20. HELP COMMAND
                        elif inPuTMsG.strip().lower() in ['/help', 'help', '/commands', 'commands', '/list', 'list', '/menu', 'menu', 'extract commands']:
                            print(f'🚀 Sending Multi-Part Help Menu to {uid}')                            
                            help_pages = ["""[B][C][00FFFF]┌──────────────┐
│   [FFFFFF] BOT COMMAND MENU    [00FFFF] │
└──────────────┘

PLAYER INFORMATION:[FFFFFF]
info [uid]   - Full player details
name [uid]   - Get player name  
bio [uid]    - Get player bio
check [uid]  - Ban status check

[00FFFF]ATTACK COMMANDS:[FFFFFF]
spam [uid]   - Invite spam attack
gali [name]  - Abuse text spam
kick [uid]   - Kick from squad
lag [t-code]   - Team lag attack

[00FFFF]TEAM CONTROL:[FFFFFF]
join [T-code]  - Join team by code
solo         - Leave current team
5            - Create 5 player group

[00FFFF]EMOTE SYSTEM:[FFFFFF]
evo          -  Random emote
x [uid] [emote]   - Play emotes 

[C][00FFFF]AI & UTILITY:[FFFFFF][/C]
/bundle [choose]  - Bot bundle
ai [msg]    - Chat with AI
/stop         - Stop all attacks
restart      - Restart bot""",

]                            
                            
                            asyncio.create_task(send_paged_help(help_pages, response.Data.chat_type, uid, chat_id, key, iv))
                            
                    
                            
                                                                            
                    #5. make 5 player group command  
                    if response:
                        # 5. MAKE 5 PLAYER GROUP COMMAND (FIXED)
                        if inPuTMsG.startswith(("5")) and (inPuTMsG == "5" or inPuTMsG.startswith("5 ")):
                            try:
                                parts = inPuTMsG.split()
                                
                                # If just "5" is sent, use sender's UID
                                if len(parts) == 1:
                                    target_uid = uid
                                # If "5 [UID]" is sent, use target UID
                                elif len(parts) >= 2:
                                    try:
                                        target_uid = int(parts[1])
                                    except:
                                        target_uid = uid
                                else:
                                    target_uid = uid
                                
                                dd = chatdata['5']['data']['16']
                                print(f'Sending invitation to {target_uid}')
                                message = f"[B][C][I]{get_random_color()}\nAccept My Invitation Fast[FF1343] ❤️\n"
                                P = await SEndMsG(response.Data.chat_type , message , target_uid , chat_id , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                                
                                PAc = await OpEnSq(key , iv,region)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , PAc)
                                
                                C = await cHSq(5, target_uid ,key, iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , C)
                                V = await SEnd_InV(5 , target_uid , key , iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , V)
                                pass
                            except:
                                print('Error in group command')                          
                        
                    #5. make 5 player group command  
                    if response:
                        # 5. MAKE 5 PLAYER GROUP COMMAND (FIXED)
                        if inPuTMsG.startswith(("4")) and (inPuTMsG == "4" or inPuTMsG.startswith("4 ")):
                            try:
                                parts = inPuTMsG.split()
                                
                                # If just "5" is sent, use sender's UID
                                if len(parts) == 1:
                                    target_uid = uid
                                # If "5 [UID]" is sent, use target UID
                                elif len(parts) >= 2:
                                    try:
                                        target_uid = int(parts[1])
                                    except:
                                        target_uid = uid
                                else:
                                    target_uid = uid
                                
                                dd = chatdata['5']['data']['16']
                                print(f'Sending invitation to {target_uid}')
                                message = f"[B][C][I]{get_random_color()}\nAccept My Invitation Fast[FF1343] ❤️\n"
                                P = await SEndMsG(response.Data.chat_type , message , target_uid , chat_id , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                                
                                PAc = await OpEnSq(key , iv,region)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , PAc)
                                
                                C = await cHSq(4, target_uid ,key, iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , C)
                                V = await SEnd_InV(4 , target_uid , key , iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , V)
                                pass
                            except:
                                print('Error in group command')          
                                
                                
                                                                                
            whisper_writer.close()
            await whisper_writer.wait_closed()
            whisper_writer = None
        
        except Exception as e:
            print(f"Error {ip}:{port} - {e}")
            whisper_writer = None
        await asyncio.sleep(reconnect_delay)
                     

# =========================================================
# MAIN FUNCTION
# =========================================================
async def MaiiiinE():
    global ACCESS_TOKEN, UID, PASSWORD

    if ACCESS_TOKEN and ACCESS_TOKEN.strip():
        # ── ACCESS TOKEN LOGIN ──────────────────────────────────
        print("[*] Access token available, token se login ho raha hai...")
        access_token = ACCESS_TOKEN.strip()

        print("[*] Inspecting access token...")
        open_id, platform = await InSpeCcToKeN(access_token)

        if not open_id:
            print("[!] Failed to get open_id from token. Check token validity.")
            return None

        print("✅ DEBUG: Token inspect successful")
        PyL = await EncRypTMajoRLoGin(open_id, access_token, platform)

    elif UID and UID.strip() and PASSWORD and PASSWORD.strip():
        # ── UID + PASSWORD LOGIN (FAST NOW) ─────────────────────
        print("[*] UID + Password se login ho raha hai (FAST MODE)...")
        open_id, access_token, platform = await GeNeRaTeAccEss(UID.strip(), PASSWORD.strip())

        if not open_id or not access_token:
            print("[!] UID/Password se login fail hua. Credentials check karo.")
            return None

        print("✅ DEBUG: Token generated successfully")
        PyL = await EncRypTMajoRLoGin(open_id, access_token, platform)

    else:
        print("[!] Koi bhi login credentials nahi mile!")
        print("    → ACCESS_TOKEN set karo, ya UID + PASSWORD set karo.")
        return None
    # ────────────────────────────────────────────────────────────
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: 
        print(" 🚫Target Account is Banned or Not Registered ! ")
        return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    region = MajoRLoGinauTh.region
    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    
    # NEW: Set bot's own UID to avoid reading bot's own messages in AI mode
    global BOT_UID
    BOT_UID = TarGeT
    
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp

    try:
        with open("token.txt", "w") as f:
            f.write(ToKen)
        print(f"✅ Bot JWT token saved to token.txt")
    except Exception as e:
        print(f"⚠️ Could not save token: {e}")

    LoGinDaTa = await GetLoginData(UrL, PyL, ToKen)
    if not LoGinDaTa: 
        print("ErroR - GeTinG PorTs From LoGin DaTa !")
        return None
    
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP, OnLineporT = OnLinePorTs.split(":")
    ChaTiP, ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    
    equie_emote(ToKen,UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), key, iv)
    ready_event = asyncio.Event()
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region))
    task2 = asyncio.create_task(TcPOnLine(OnLineiP, OnLineporT, key, iv, AutHToKen))  
    task3 = asyncio.create_task(PeriodicStateReset())

    os.system('clear')
    
    print("    🤖 VINNY BOT - INITIALIZING")
    print("\n📡 Connecting to Free Fire servers...")
    print("\n┌────────────────────────────────────┐")
    print("│ █████████████░░░░░░░░░░░░░░░░░░ │")
    print("└────────────────────────────────────┘")
    time.sleep(0.3)
    os.system('clear')
    
    print("    🤖 VINNY BOT - INITIALIZING")
    print("\n🔐 Authenticating with servers...")
    print("\n┌────────────────────────────────────┐")
    print("│ ██████████████████████░░░░░░░░░░░░ │")
    print("└────────────────────────────────────┘")
    time.sleep(0.3)
    os.system('clear')
    print("    🤖 VINNY BOT - INITIALIZING")
    print("\n🌐 Establishing connections...")

    print("\n┌────────────────────────────────────┐")
    print("│ ██████████████████████████████████ │")
    print("└────────────────────────────────────┘")
    time.sleep(0.3)
    os.system('clear')

    # NEW PURPLE GRADIENT LOGO
    show_logo()
    print("\n" + "—"*50)
    print("✅ BOT STATUS: ONLINE")
    print("—"*50)
    print(f"\n📱 TARGET UID : {TarGeT}")
    print(f"👤 BOT NAME   : {acc_name}")
    print(f"🌐 Server     : {region}") 
    print(f"🔐 TOKEN      : \033[1m{ToKen}")
    print("\n" + "—"*50)
    print("💀 READY FOR COMMANDS")
    print("—"*50 + "\n")
    # ============================================================
    # 📤 AUTO FRIEND REQUEST SENDER (SILENT MODE)
    # ============================================================
    global AUTO_FRIEND_REQUEST_UIDS
    
    if AUTO_FRIEND_REQUEST_UIDS and len(AUTO_FRIEND_REQUEST_UIDS) > 0:
        from xC4 import add_friend, save_bot_token_to_file
        
        # Save current token for add_friend function
        save_bot_token_to_file(ToKen)
        
        # Send friend requests silently (no output)
        for target_uid in AUTO_FRIEND_REQUEST_UIDS:
            try:
                add_friend(target_uid)
                await asyncio.sleep(0.5)  # Small delay between requests
            except:
                pass  # Silently ignore errors
    # ============================================================
    
    await asyncio.gather(task1, task2, task3)

async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE(), timeout=7 * 59 * 50)
        except asyncio.TimeoutError:
            print("Token Expired, Restarting")
        except KeyboardInterrupt:
            # Silent exit — handled in main block
            break
        except Exception as e:
            print(f"Trying to start bot Restarting ...")

if __name__ == '__main__':
    try:
        asyncio.run(StarTinG())
    except KeyboardInterrupt:
        # Clean shutdown message
        print("\n\033[91m Bot stopped by admin\033[0m")
        sys.exit(0)