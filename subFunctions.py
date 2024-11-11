
import diskReadandSearch as drs
import datetime
import psutil

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
    
def show(opt):
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

def getMultilineInput():
    print("Enter your python code. Blank enter for finish: ")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)

def executeCode(code_string):
    try:
        localNamespace = {} # 코드를 실행하기 전에 로컬 네임스페이스를 생성
        exec(code_string, {"__builtins__": __builtins__}, localNamespace) # exec를 사용하여 여러 줄의 코드 실행
        print('Process successfully finished.')
    except Exception as e:
        print(f"Error: {e}")