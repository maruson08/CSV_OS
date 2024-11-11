import diskReadandSearch as drs
import datetime
import psutil

#현재 위치
global curPath
curPath = 'o'
disk = 'disk.csv'

def moveDir(path): # 현재 경로 이동
    global curPath
    curPathList = curPath.split('/')
    if path =='.':
        if curPath == 'o':
            return
        else:
            curPath = 'o'
            for i in range(1, len(curPathList)-1):
                curPath = curPath + '/' + curPathList[i]
            return

    isPathExist = drs.findDir(curPath + '/' + path)
    curDepth = len(curPath.split('/'))-1
    if  isPathExist == (None, None):
        return
    else:
        if path == 'o':
            curPath = 'o'
        else:
            curPath = curPath+'/'+path
        return
    
def show(opt): # datetime 라이브러리 사용해 시간, 날짜, psutil 사용해 노트북 배터리 출력
    if opt == 'time':
        print(datetime.datetime.now().strftime('%H : %M : %S'))
    elif opt == 'date':
        print(datetime.datetime.today())
    elif opt == 'battery':
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = str(battery.percent)
        plugged = "Plugged In" if plugged else "Not Plugged In"
        print(percent+'% | '+plugged)
    else:
        print(f'Function show can\'t show {opt}')

def getMultilineInput(): # 파이썬 코드를 입력받기 위한 함수 여러 줄 입력 가능
    print("Enter your python code. Blank enter for finish: ")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)

def executeCode(code_string): # getMultilineInput 함수에서 받은 코드를 실행하는 함수
    try:
        localNamespace = {} # 코드를 실행하기 전에 로컬 네임스페이스를 생성
        exec(code_string, {"__builtins__": __builtins__}, localNamespace) # exec를 사용하여 여러 줄의 코드 실행
        print('Process successfully finished.')
    except Exception as e:
        print(f"Error: {e}")

# CLI 명령어 딕셔너리
command = {
    "movedir": {"function": moveDir, "args": "prompt[1]"},
    "createdir": {"function": drs.createFolders, "args": "curPath, prompt[1]"},
    "deletedir": {"function": drs.deleteFolders, "args": "curPath + '/' +prompt[1]"},
    "create": {"function": drs.createDoc, "args": "curPath, prompt[1]"},
    "delete": {"function": drs.deleteDoc, "args": "curPath + '/' +prompt[1]"},
    "modify": {"function": drs.modifyDoc, "args": "curPath + '/' +prompt[1]"},
    "read": {"function": drs.readDoc, "args": "curPath + '/' +prompt[1]"},
    "tree": {"function": drs.tree, "args": "curPath"},
    "show": {"function": show, "args": "prompt[1]"},
    "disk": {"function": print, "args": "'total', str(os.path.getsize(disk)), 'byte using'"}, # 디스크 csv 메모리량 측정
    "python": {"function": executeCode, "args": "getMultilineInput()"}
}

while True:
    # try:
        print()
        prompt = input(f'{curPath}>>').split(' ')
        if prompt[0] not in command: # 명령어 존재 여부 확인
            print(f"'{prompt[0]}' is not recognized as an internal or external command, operable program or batch file.")
            continue
        if len(prompt)>2:
            print(f"'{prompt[0]}' doesn't support argument {prompt[1:]}")
        args = eval(command[prompt[0]]['args'])

        if not isinstance(args, tuple): # 매개 변수가 하나일때 반환 타입을 튜플로 맞춰주기 위한 코드
            args = (args,) # 단일 튜플 생성

        command[prompt[0]]['function'](*args) # 함수실행
        
    # except Exception as e:
    #     print(f"System Error: {e}")