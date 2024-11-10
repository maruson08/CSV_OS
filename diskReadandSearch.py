import csv
import datetime
import pandas as pd
# 파일 내용을 리스트로 저장
def findfile(path): #파일의 상위 폴더, 파일명을 입력받았을때 폴더가 있는 줄의 몇번째 인덱스에 파일이 존재하는지 반환하는 함수 
    split_path=path.split("/")
    filename=split_path.pop() #경로의 마지막을 파일 이름으로 반환
    folder='/'.join(split_path) #상위 폴더 경로 문자열로 변환
    folderlinenum=movedir(folder)[0] #폴더 위치 반환
    with open('disk.csv','r',newline='') as file:
        reader=csv.reader(file)
        lines=list(reader)
    findfolder=False
    file_idx=0
    for text in lines[folderlinenum]: #삭제할 파일 상위 폴더의 첫번쨰 파일이 있는 줄부터 순회하여 삭제할 파일을 찾음
        if findfolder:
            dic_text=eval(text) #문자열을 딕셔너리로 변환
            if dic_text['filename']==filename:
                return file_idx
        if text!='':
            findfolder=True
        file_idx+=1
    print('파일이 존재하지 않습니다. 다시 확인해주세요')
    return None

def movedir(path):
    with open('disk.csv', 'r') as d:
        disk = list(csv.reader(d))
        linenum = 0  # 줄 번호
        dir_parts = path.split('/')  # 찾으려는 경로 분리
        target_depth = len(dir_parts) - 1  # 찾으려는 깊이
        foundlastfolder=False
        for line in disk:
            # 현재 줄에서 깊이 계산 (빈 셀의 개수로 깊이 파악)
            current_depth = 0 
            for i in line:
                if i=='':
                    current_depth+=1
                    continue
                break
            # 현재 깊이와 일치하는 경로를 찾고 있는지 확인
            if current_depth < target_depth and line[current_depth] == dir_parts[current_depth]:
                # 현재 부분 경로가 일치할 때, 깊이 증가
                current_depth += 1

            elif current_depth == target_depth and line[current_depth] == dir_parts[current_depth]:
                # 찾고자 하는 전체 경로가 일치하는 경우 줄 번호 출력
                startlinenum=linenum
                foundlastfolder=True

            if foundlastfolder: #지울 폴더 하위 폴더까지 지우려면 eod 나오는 라인도 찾아야함
                if line[target_depth]=='EOD'or line[target_depth]=='EOM':
                    lastlinenum=linenum
                    return startlinenum,lastlinenum
            linenum += 1
        print("Path not found")
        return None,None
    
def check_correctname(path,new_filename):
    if '/' in new_filename:
        print('폴더명에는 /가 들어갈 수 없습니다.')
        return False
    split_extension=new_filename.split(".") #확장자명 구분
    if len(split_extension)!=2:
        print('파일명이 올바르지 않습니다. 확장자를 제대로 입력해주세요')
        return False
    startfilenum=movedir(path)[0]
    findfolder=False
    with open('disk.csv','r',newline='') as file:
        reader=csv.reader(file)
        lines=list(reader)
        for text in lines[startfilenum]: #동일명의 파일이 있는지 확인
            if findfolder:
                dic_text=eval(text)
                if dic_text['filename']==new_filename:
                    print('이미 같은 이름의 파일이 존재합니다. 다른 파일명을 입력해주세요')
                    return False
            if text!='':
                findfolder=True
    return True

def createFolders(path, new_filename): #설치 위치, 파일명 받음
    if '/' in new_filename:
        print('폴더명에는 /가 들어갈 수 없습니다.')
        return
    startfilenum, lastfilenum=movedir(path)[0], movedir(path)[1]
    if movedir(path)[0]==None:
        print('경로명이 잘못됨')
        return
    with open('disk.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        lines = list(reader)
    for i in range(startfilenum, lastfilenum+1):
        for foldername in lines[i]:
            if foldername==new_filename:
                print('이미 같은 파일명이 있습니다. 다른걸로 해주세요')
                return 0
            if foldername!='': #프로그램 작동 시간 줄이려고 한 줄의 첫번째 칸 텍스트만 읽음
                break

    deep = path.split('/')
    csv_file=[]
    for i in range(len(deep)):
        csv_file.append('') # 어떤 폴더에 들어가 있는지 표기하려면 새 리스트 앞에 ''추가해줘야함
    csv_file.append(new_filename)

    EOD=[]
    for i in range(len(deep)):
        EOD.append('')
    EOD.append('EOD')
    

    lines.insert(startfilenum+1, csv_file) #폴더 있는 줄 한칸 아래에 삽입
    lines.insert(startfilenum+2, EOD) #eod 있는 줄 삽입


    with open('disk.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines)
        print('성공적으로 폴더 생성을 마쳤습니다.')
        return
    print('오류 발생. disk 파일을 확인해주세요')


def deleteFolders(path):
    if movedir(path)[0]==None:
        print('경로명이 잘못됨')
        return
    startfilenum,lastfilenum=movedir(path)
    with open('disk.csv','r',newline='') as file:
        reader=csv.reader(file)
        lines=list(reader)

    for i in range(lastfilenum+1, startfilenum, -1):
        del lines[i-1]  # 지울 폴더의 eod라인과 폴더명 적힌 라인까지 삭제

    with open('disk.csv', 'w',newline='') as file:
        writer=csv.writer(file)
        writer.writerows(lines)
        print('성공적으로 폴더 삭제를 마쳤습니다')
        return
    print('오류 발생. disk 파일을 확인해주세요')

def createDoc(path,new_filename): #설치 위치, 이름, 내용 입력
    if movedir(path)[0]==None:
        print('경로명이 잘못됨')
        return
    split_extension=new_filename.split(".")
    if len(split_extension)!=2:
        print('파일명이 올바르지 않습니다. 확장자를 제대로 입력해주세요')
        return
    if split_extension[1]!='txt' and split_extension[1]!='csv':
        print('지원하지 않는 확장자 입니다. 현재는 txt나 csv만 지원하고 있습니다.')
        return
    startfilenum=movedir(path)[0]
    findfolder=False
    with open('disk.csv','r',newline='') as file:
        reader=csv.reader(file)
        lines=list(reader)
        for text in lines[startfilenum]: #동일명의 파일이 있는지 확인
            if findfolder:
                dic_text=eval(text)
                if dic_text['filename']==new_filename:
                    print('이미 같은 이름의 파일이 존재합니다. 다른 파일명을 입력해주세요')
                    return
            if text!='':
                findfolder=True
    content=''
    split_extension=new_filename.split(".") #확장자명 구분
    print('저장하고 싶은 내용을 한줄씩 입력해주세요. 입력이 끝나면 enter를 눌러 입력을 마치세요')
    while True: #내용 입력
        line = input()
        if not line:
            break
        content=content+line+'\n'

    new_text = str({'filename':new_filename,'dateCreated':datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),'dateLastModified': datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), 'content': content})
    lines[startfilenum].append(new_text)

    
    with open('disk.csv', 'w',newline='') as file:
            writer=csv.writer(file)
            writer.writerows(lines)
            print('성공적으로 파일이 생성되었습니다.')
            return
    print('오류 발생. disk 파일을 확인해주세요')


def deleteDoc(path):
    split_path=path.split("/")
    del_filename=split_path.pop() #경로의 마지막을 파일 이름으로 반환
    del_folder='/'.join(split_path) #상위 폴더 경로 문자열로 변환
    folderlinenum=movedir(del_folder)[0] #폴더 위치 반환
    if '/' in del_filename:
        print('폴더명에는 /가 들어갈 수 없습니다.')
        return
    with open('disk.csv','r',newline='') as file:
        reader=csv.reader(file)
        lines=list(reader)
    del_idx=findfile(path)
    if del_idx==None:
        return
    lines[folderlinenum].pop(del_idx)
    with open('disk.csv', 'w',newline='') as file:
        writer=csv.writer(file)
        writer.writerows(lines)
        print('성공적으로 파일을 삭제했습니다')
        return
    print('오류 발생. 정상적으로 파일 삭제가 이루어지지 않았습니다.')

def modifyDoc(path):
    split_path=path.split("/")
    mod_filename=split_path.pop() #경로의 마지막을 파일 이름으로 반환
    mod_folder='/'.join(split_path) #상위 폴더 경로 문자열로 변환
    folderlinenum=movedir(mod_folder)[0] #폴더 위치 반환
    mod_idx=findfile(path)
    if folderlinenum==None or mod_idx==None:
        print('경로가 잘못되었습니다. 확인해주세요')
        return
    new_filename=input('enter the new name for this file. if you do not change the name, please press enter ')
    if new_filename!='':
        if not check_correctname(mod_folder,new_filename):
            return
        with open('disk.csv','r',newline='') as file:
            reader=csv.reader(file)
            lines=list(reader)
        mod_line=eval(lines[folderlinenum][mod_idx])
        mod_line['filename']=new_filename
        lines[folderlinenum][mod_idx]=mod_line
    new_filetext=''
    print('저장하고 싶은 내용을 한줄씩 입력해주세요. 입력이 끝나면 enter를 눌러 입력을 마치세요')
    while True: #내용 입력
        line = input()
        if not line:
            break
        new_filetext=new_filetext+line+'\n'
    with open('disk.csv','r',newline='') as file:
        reader=csv.reader(file)
        lines=list(reader)
    eval(lines[folderlinenum][mod_idx])
    mod_line['content']=new_filetext
    mod_line['dateLastModified']=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    lines[folderlinenum][mod_idx]=mod_line
    with open('disk.csv', 'w',newline='') as file:
        writer=csv.writer(file)
        writer.writerows(lines)
        print('성공적으로 파일을 수정했습니다')
        return
    print('오류 발생. 정상적으로 파일 수정이 이루어지지 않았습니다.')

def readDoc(path):
    split_path=path.split("/")
    read_filename=split_path.pop() #경로의 마지막을 파일 이름으로 반환
    read_folder='/'.join(split_path) #상위 폴더 경로 문자열로 변환
    folderlinenum=movedir(read_folder)[0] #폴더 위치 반환
    read_idx=findfile(path)
    with open('disk.csv','r',newline='') as file:
        reader=csv.reader(file)
        lines=list(reader)
    readline=eval(lines[folderlinenum][read_idx])
    content=readline['content'].split('\n')
    extension=readline['filename'].split('.')[1]
    if extension=='txt':
        while content:
            print(content[0])
            content.pop(0)
    elif extension=='csv':
        csv_content=[]
        for text in content:
            csv_content.append(text.split(','))
        csv_content=pd.DataFrame(csv_content)
        csv_content = csv_content.fillna("")
        print(csv_content)

readDoc('o/folder2/testfolder/test.csv')