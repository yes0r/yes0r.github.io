---
title: "리눅스 기반 시스템 탐색 및 데이터 분석(OverTheWire Bandit)"
date: 2026-05-13 15:27:48 +0900
categories: ["블로그/기술문서"]
tags: ["Tistory", "Linux", "OverTheWire", "Bandit"]
render_with_liquid: false
---

> Original: [https://yeseul7.tistory.com/28](https://yeseul7.tistory.com/28)

본 실습은 MacBook의 macOS 환경에서 진행하였다.
macOS는 기본적으로 UNIX 기반 터미널 환경을 지원하므로, Windows 환경에서 사용하는 WSL 대신 기본 터미널(zsh)을 활용하여 Bandit 서버에 접속하고 실습을 수행하였다.





## Level 0

목표:  SSH를 사용하여 게임에 로그인하는 것

포트와, 연결할 호스트, 사용자의 이름, 비밀번호까지 다 주어졌다.



```
ssh -p 2220 bandit0@bandit.labs.overthewire.org
```





![](/assets/img/posts/tistory/tistory-28-01.png)



접속 완료



## Level 0 → Level 1

목표: 홈 디렉토리에 있는 readme 파일에서 다음 레벨(bandit1)의 비밀번호를 찾는 것





```
ls #파일 보기
cat readme #파일의 목록 중 readme 읽기 (파일 읽기)
```



ls와 같은 명령어를 이용해서 readme 파일의 존재를 확인 후, cat readme를 통해 읽으면 다음 레벨의 password를 찾아볼 수 있게 된다.

![](/assets/img/posts/tistory/tistory-28-02.png)



문제에서 말했듯 일단 password (ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If)를 복사해서 저장해둔다



![](/assets/img/posts/tistory/tistory-28-03.png)



exit 명령어를 통해 로그아웃 한 뒤 찾은 암호로 다시 접속한다.





## Level 1 → Level 2



목표: 홈 디렉토리에 있는 -라는 이름의 파일을 읽어서 다음 레벨 비밀번호를 찾는 것



하지만, 리눅스에서는 -가 특수하게 쓰이기 때문에 cat -를 할 때, 이상하게 작용할 수 있음.

그러므로 ls를 통해 파일명을 확인 한 후, ./를 통해 파일명을 지정하며 알아내야함.



리눅스에서 ./파일명은 현재 폴더 안의 파일이라는 뜻이므로, ./를 이용하면 -도 파일명으로 선택 가능



```
ls
# - 가 들어있음

cat ./-
```



![](/assets/img/posts/tistory/tistory-28-04.png)





263JGJPfgU6LtdEvgfWU1XP5yac29mFx 다음 단계의 비밀번호를 저장해둔 후, 아까와 같이 exit -> 암호로 다시 접속



## Level 2 → Level 3



목표: 홈 디렉토리에 있는 spaces in this filename 이라는 파일에서 다음 레벨의 비밀번호를 찾기



파일 이름 안에 공백이 들어가 있는 경우 리눅스에서는 공백을 명령어 인자 구분으로 인식하기 때문에, 공백으로 인해 파일명이 잘려버리는 이슈가 발생. 그러므로 전체를 하나로 묶어주기 위해 ""를 사용하여야만 한다.



```
ls
cat "./--spaces in this filename--"
```





![](/assets/img/posts/tistory/tistory-28-05.png)

실제 파일 이름은 --spaces in this filename-- 이기 때문에, 파일명이 -로 시작할 경우 옵션으로 인식될 수 있으므로, 이전 레벨과 마찬가지로 ./를 사용하여 현재 디렉토리의 파일임을 명확히 지정해주어야 한다.



비밀번호: MNk8KNH3Usiio41PRUEoDFPqfxLPlSmx



## Level 3 → Level 4



목표: inhere 디렉토리 안에 있는 숨김 파일(hidden file)에서 다음 레벨의 비밀번호를 찾는 문제



리눅스에서는 . 으로 시작하는 파일을 숨김 파일로 취급하기 때문에, 일반 ls 명령어로는 보이지 않는다.



```
cd inhere
ls -a
cat ...Hiding-From-You
```



파일이  inhere 디렉토리 안에 있기 때문에 우선 디렉토리 이동을 할때 쓰는 cd를 통해 이동 후,

 ls -a를 통해 숨김 파일까지 확인해야만 한다. -a를 붙이는 이유는, a가 all을 뜻하며, 숨김 파일까지 모두 보여주게 만드는 명령어이기 때문이다.



![](/assets/img/posts/tistory/tistory-28-06.png)



비밀번호: 2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ



## Level 4 → Level 5



목표: inhere 디렉토리 안에 있는 여러 파일 중, 사람이 읽을 수 있는(human-readable) 파일 하나를 찾아 다음 레벨의 비밀번호를 획득



리눅스에는 텍스트 파일, 뱌이너리 파일, 이미지, 압축 파일 등 다양한 파일이 있지만, 사람이 읽을 수 있는 파일은 정상 문자로 보이는 텍스트로, 사람이 읽을 수 없는 바이너리 파일 같은 것은 깨져 보인다.



```
cd inhere
ls
file ./*
```



inhere 디렉토리 안에 있다고 했기 때문에, cd imhere을 통해 디렉토리로 이동, ls를 통해 파일이 무엇이 있는지 확인한 후,

file ./* 명령어를 통해 현재 디렉토리의 모든 파일의 종류를 분석한다.



여기서, file은 이 파일이 어떤 종류인지 분석해주는 명령어이고, *는 모든 파일이라는 뜻이라서, ./*를 해주면 현재 디렉토리의 모든 파일을 의미한다. 그래서 file ./*를 하면 현재 디렉토리의 모든 파일을 어떤 종류인지 분석을 해주게 된다.





![](/assets/img/posts/tistory/tistory-28-07.png)



-file07이 text 파일로 나타나있기 때문에 cat ./-file07을 해주면,



비밀번호: 4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw

가 나타나게 된다.





## Level 5 → Level 6



목표: inhere 디렉토리 아래 어딘가에 있는 파일 중, 특정 조건을 모두 만족하는 파일을 찾아 다음 레벨의 비밀번호를 획득



특정 조건을 모두 만족하는 파일을 찾아야 하는 문제이다. 즉, 하나씩 찾기보다는 find를 쓰는 것이 출제 의도에 더욱 맞는 풀이이다.

find는 파일을 조건으로 검색하는 명령어이다. -size 등 옵션을 이용해 조건으로 검색을 할 수가 있다.



```
cd inhere
find . -size 1033c #문제에서 말한 조건, 크기가 정확히 1033 bytes인 파일을 찾기 위함

#size로 파일 크기 검색,
#리눅스에서 c는 bytes를 의미하며,
#.는 현재 디렉토리를 의미한다.

file ./maybehere07/.file2
#나온 ./maybehere07/.file2 파일의 종류를 확인
```



![](/assets/img/posts/tistory/tistory-28-08.png)





## Level 6 → Level 7



목표: 서버 전체에서 특정 조건을 만족하는 파일을 찾아, 그 안에 저장된 다음 레벨의 비밀번호를 획득



조건은, 소유자가 bandit7 그룹이 bandit6, 파일 크기가 33 bytes여야 한다.

리눅스 파일에는 파일 이름, 크기, 소유자, 그룹, 권한 같은 정보가 있기 때문에 find 명령어를 통해 그중 owner, group, size 조건을 사용해야한다.



주요 옵션은 다음과 같다

<table>
  <tbody>
    <tr>
      <td>-user</td>
      <td>파일 소유자</td>
    </tr>
    <tr>
      <td>-group</td>
      <td>파일 그룹</td>
    </tr>
    <tr>
      <td>-size</td>
      <td>파일 크기</td>
    </tr>
  </tbody>
</table>



조건을 추가해본다면,

```
find / -user bandit7 -group bandit6 -size 33c
```

여기서 /는 리눅스 루트 디렉토리를 뜻한다. 그러므로 find /는 서버 전체 검색의 의미.



![](/assets/img/posts/tistory/tistory-28-09.png)



많이 나오는 것 중에 권한 없는 폴더 접근 실패 메시지인 Permission denied가 없는 bandit7.password 파일을 찾았다.

cat /var/lib/dpkg/info/bandit7.password 해서 열어주면



![](/assets/img/posts/tistory/tistory-28-10.png)



다음과 같은 비밀번호 morbNTDkSW6jIlUc0ymOdMaLnOlFVAaj를 찾을 수 있다.



## Level 7 → Level 8



목표: data.txt 파일 안에서 millionth 라는 단어 옆에 있는 값을 찾아 다음 레벨의 비밀번호를 획득



millionth 라는 단어 옆에 있는 값을 찾아야 하기 때문에, 파일 안에서 특정 문자열을 검색하는 명령어인 grep이 필요하다.



```
grep millionth data.txt
```

이런 구조를 통해 특정 문자열을 검색할 수가 있게 되는데,



각각의 의미는 다음과 같다.

<table>
  <tbody>
    <tr>
      <td>grep</td>
      <td>문자열 검색</td>
    </tr>
    <tr>
      <td>millionth</td>
      <td>찾을 단어</td>
    </tr>
    <tr>
      <td>data.txt</td>
      <td>검색 대상 파일</td>
    </tr>
  </tbody>
</table>



![](/assets/img/posts/tistory/tistory-28-11.png)

바로 grep을 통해 찾아주면, 다음과 같은 글자가 뜬다. millionth라는 단어가 있는 줄을 찾은 것이고, 그 옆에 비밀번호 값이 있다고 했으니



비밀번호는 dfwvzFQi4mU0wfNbFOe9RoWskMLg7eEc가 된다.





## Level 8 → Level 9

목표: data.txt 파일 안에서 단 한 번만 등장하는 줄을 찾아, 그 값을 다음 레벨의 비밀번호로 사용



한 번만 등장하는 줄을 찾아야 하기 때문에 여러 번 반복되는 줄은 제외하고 데이터를 찾아야만 한다.

잘 찾기 위해서 텍스트를 정렬하는 명령어인 sort과 중복 줄 처리 명령어인 uniq가 필요하다.



uniq만 쓰는게 아니라 sort도 함께 쓰는 이유는, uniq는 정렬이 필요하기 때문이다.

uniq는 바로 옆 줄이 같은 경우만 처리 가능하기 때문에 꼭 정렬을 해주어야 한다.



```
sort data.txt | uniq -u

#uniq -u는 리눅스에서 한 번만 나온 줄만 출력이라는 의미를 가지고 있고,
#|(pipe)를 통해서 한 명령어 결과를 다음 명령어로 전달하게 된다
```



각각의 의미를 해석해보면 다음과 같다.

<table>
  <tbody>
    <tr>
      <td>sort data.txt</td>
      <td>파일 내용 정렬</td>
    </tr>
    <tr>
      <td>|</td>
      <td>명령어 결과를 다음 명령어로 전달</td>
    </tr>
    <tr>
      <td>uniq -u</td>
      <td>한 번만 나온 줄 출력</td>
    </tr>
  </tbody>
</table>



![](/assets/img/posts/tistory/tistory-28-12.png)



비밀번호: 4CKMh1JI91bUIZZPXDqGanal4xvAg0JM



## Level 9 → Level 10



목표: data.txt 파일 안의 사람이 읽을 수 있는 문자열 중, 여러 개의 = 문자 뒤에 있는 값을 찾아 다음 레벨의 비밀번호를 획득



사람이 읽을 수 있는 문자열만 추출하는 것이 목표이기 때문에, data.txt가 일반 txt 파일이 아니라 이상한 문자들이 섞인 바이너리 데이터가 있을 것이라고 추측 할 수가 있다.



이럴 때는 어떻게 해야할까? 파일 안에서 사람이 읽을 수 있는 문자열만 추출하는 명령어인 strings을 써보면 된다.

![](/assets/img/posts/tistory/tistory-28-13.png)



문제에서는 preceded by several '=' characters이라고 했기 때문에, ===== 같은 문자 뒤에 비밀번호가 있을 확률이 높다. 먼저 사람이 읽을 수 있는 문자열 추출하고, 그 뒤에 = 포함 줄을 찾아보는 것이 좋다.



```
strings data.txt
```

이 명령어만 사용해도

![](/assets/img/posts/tistory/tistory-28-14.png)

내리다 보면 비밀번호로 추측할 수 있는 줄이 나타나지만, 더 확실히 알기 위해서



```
strings data.txt | grep ==
```

을 통해서 특정 문자열을 검색해본다.



![](/assets/img/posts/tistory/tistory-28-15.png)



the password is FGUW5ilLVJrxX9kMYMmlN4MgbpfMiqey.

즉, 비밀번호는 FGUW5ilLVJrxX9kMYMmlN4MgbpfMiqey이다.





## Level 10 → Level 11

목표: data.txt 파일 안에 Base64로 인코딩된 데이터가 들어 있으며, 이를 디코딩해서 다음 레벨의 비밀번호를 찾기



인코딩된 문자열을 원래 내용으로 되돌려야 하는데, 여기 나오는 Base64는 암호화가 아니라 인코딩이기 때문에, 데이터를 사람이 복사하거나 전송하기 쉬운 문자 형태로 바꿔둔 것이라고 생각하면 된다.



```
cat data.txt
```



cat을 통해 열어보면

![](/assets/img/posts/tistory/tistory-28-16.png)



다음과 같은 문자열이 있는데, 끝에 = 또는 ==가 붙어 있으면 Base64일 가능성이 높아진다.



```
base64 -d data.txt #Base64를 디코딩
```



-d 옵션을 통해 디코딩 해주면

![](/assets/img/posts/tistory/tistory-28-17.png)



비밀번호 dtR173fZKb0RRsDFSGsg2RWnpNVj3qRr가 된다.



## Level 11 → Level 12

목표: data.txt 파일 안에 있는 문자는 알파벳이 13칸씩 밀려 있는 상태. 이를 원래대로 되돌려 다음 레벨의 비밀번호를 찾기



이 문제를 풀기 위해선 ROT13에 대해서 알아야한다.

ROT13은 알파벳을 13칸씩 밀어서 바꾸는 방식으로, 한 번 더 ROT13을 적용하면 원래 문자로 돌아온다는 특징이 있다.



lowercase(a-z)와 uppercase(A-Z)가 13 positions rotated라고 적혀있기 때문에, A-Z와 a-z를 둘 다 처리해야하고, 치환을 위해 특정 문자들을 다른 문자들로 바꿔주는 명령어인 tr이 쓰이게 된다.



```
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```





각각의 의미는 다음과 같다.

<table>
  <tbody>
    <tr>
      <td>cat data.txt</td>
      <td>data.txt 내용 출력</td>
    </tr>
    <tr>
      <td>|</td>
      <td>명령어의 결과를 뒤로 넘김</td>
    </tr>
    <tr>
      <td>tr</td>
      <td>문자 치환</td>
    </tr>
    <tr>
      <td>'A-Za-z'</td>
      <td>대문자 A-Z, 소문자 a-z 전체</td>
    </tr>
    <tr>
      <td>'N-ZA-Mn-za-m'</td>
      <td>13칸 밀린 알파벳 순서</td>
    </tr>
  </tbody>
</table>

![](/assets/img/posts/tistory/tistory-28-18.png)







비밀번호: 7x16WNeHIi5YkIhWsfFIqoognUTyj9Q4



## 12 → Level 13



목표: data.txt 파일은 어떤 파일을 hexdump 형태로 바꿔놓은 것, 그 원본 파일은 여러 번 압축되어 있는데, 이 hexdump를 다시 원래 파일로 복구한 뒤, 압축을 여러 번 풀어서 다음 레벨의 비밀번호를 찾기



data.txt는 파일 내용을 16진수 형태로 보여주는 hexdump의 형태라고 한다. 실제 압축 파일이 아니라, 압축 파일을 사람이 볼 수 있는 16진수 텍스트로 바꿔둔 상태라는 뜻. hexdump를 원래 바이너리 파일로 되돌리는 것이 중요하다.





우선, 명령어를 통해 원래 바이너리 파일로 되돌리고 /tmp 아래에 작업용 디렉토리를 만들어서 거기서 작업하라고 안내하고 있기 때문에



```
mktemp -d
```

명령어를 통해 임시 디렉토리를 만든다. 여기서 임시 디렉토리를 만드는 이유는, 압축을 여러 번 풀게 되면 파일 이름도 바꾸고 새 파일도 생기기 때문에 Bandit 홈 디렉토리에서 마음대로 파일을 만들거나 수정하기 힘들 수도 있어서이다.







![](/assets/img/posts/tistory/tistory-28-19.png)



다음과 같은 임시 디렉토리가 만들어지면



```
cd /tmp/tmp.To4YfkYWCb
```

cd를 통해 그곳에 들어가고,



```
cp ~/data.txt .

#cp(copy) : cp 원본파일 복사할 위치 형식으로 쓰인다.
#~는 현재 로그인한 bandit12의 홈 디렉토리
#.은 현재 디렉토리
```

명령어를 통해 홈 디렉토리에 있는 data.txt를 현재 작업 폴더로 복사한다.



ls로 파일이 있는 것을 확인해준 뒤,

```
xxd -r data.txt data

#xxd는 파일을 hex dump 형태로 보여주거나, 반대로 hex dump를 원래 바이너리 파일로 되돌리는 명령어
#-r은 reverse, 되돌리기라는 뜻
```



다음과 같은 명령어를 통해서 hexdump을 복구한다. 이후 file data를 통해 어떤 압축을 풀어야 하는지 확인을 해보면,



![](/assets/img/posts/tistory/tistory-28-20.png)



gzip 압축 파일임을 확인할 수 있게 된다. 그 이후

```
mv data data.gz #.gz여야 풀기 편하기 때문에 mv를 통해 이름 변경
gzip -d data.gz #압축 해제
file data #어떤 종류의 파일인지 확인
```



file로 종류 확인하고, 맞는 압축 해제 명령어 사용 후 다시 file로 확인하는 과정을 반복하면 된다.



![](/assets/img/posts/tistory/tistory-28-21.png)





마지막 text 파일 확인 후 cat을 하면 드디어 비밀번호를 알 수가 있다.



비밀번호: FO5dwFsc0cbaIiH0h8J2eUks2vdTDwAn



## Level 13 → Level 14



목표: 다음 레벨의 비밀번호는 /etc/bandit_pass/bandit14에 저장되어 있지만, 해당 파일은 bandit14 사용자만 읽을 수 있다. 이번 레벨에서는 비밀번호 대신 다음 레벨에 접속할 수 있는 SSH 개인키가 제공. SSH 개인키를 받기.



비밀번호 대신 SSH key를 이용해서 로그인해야 하기 때문에, 우선 key가 있는 파일을 찾아야한다.



![](/assets/img/posts/tistory/tistory-28-22.png)



ls를 통해 파일을 살펴보면 sshkey.private라는 파일을 찾을 수 있다.



현재 환경에서 시도해본 결과 Bandit 서버 내부에서 localhost로 다시 접속하는 방식이 차단되어 있었다. 따라서 sshkey.private 파일의 내용을 로컬 Mac 환경에 저장한 뒤, 해당 개인키를 사용하여 외부에서 bandit14 계정으로 접속하는 방식으로 진행하였다.



```
cat sshkey.private
```





![](/assets/img/posts/tistory/tistory-28-23.png)



보이는 key값을 복사해둔 뒤에 exit한 후, mac에서 키 파일을 만든다.

```
nano ~/bandit14.key #nano는 터미널에서 쓰는 간단한 텍스트 편집기이다.
```





<table>
  <tbody>
    <tr>
      <td>nano</td>
      <td>터미널에서 쓰는 간단한 텍스트 편집기</td>
    </tr>
    <tr>
      <td>~</td>
      <td>내 홈 디렉토리</td>
    </tr>
    <tr>
      <td>/</td>
      <td>경로 구분자</td>
    </tr>
    <tr>
      <td>bandit14.key</td>
      <td>만들거나 열 파일 이름</td>
    </tr>
  </tbody>
</table>



홈 디렉토리에 있는 bandit14.key 파일을 nano로 열고, 파일이 없으면 새로 만들어주는 명령어가 된다.





![](/assets/img/posts/tistory/tistory-28-24.png)



안으로 돌아가 키를 붙여넣어주고,



![](/assets/img/posts/tistory/tistory-28-25.png)



SSH 개인키 파일은 인증 정보이기 때문에 권한이 과도하게 열려 있으면 SSH에서 사용을 거부할 수 있다. chmod 600 ~/bandit14.key 명령어를 사용해서 개인키 파일의 권한을 소유자만 읽고 쓸 수 있는 상태로 제한해주었다.

```
chmod 600 ~/bandit14.key
#chmod는 파일 권한을 변경하는 명령어
#600 소유자만 읽기/쓰기 가능, 다른 사용자는 접근 불가

ssh -i ~/bandit14.key -p 2220 bandit14@bandit.labs.overthewire.org
```



다음과 같이 개인키 파일을 이용해 접속을 시도하면







![](/assets/img/posts/tistory/tistory-28-26.png)

 다음과 같이 비밀번호 입력 없이 드디어 bandit14 계정으로 접속할 수 있다.





##  Level 14 → Level 15

목표: 현재 레벨의 비밀번호를 localhost의 30000번 포트로 제출해 다음 레벨의 비밀번호를 획득.



우선 현재 레벨의 비밀번호에 대해 알아보았다.



이전 레벨의 설명에서 bandit14의 비밀번호가 `/etc/bandit_pass/bandit14`에 저장되어 있으며, bandit14 사용자만 읽을 수 있다고 안내되어 있었다. SSH 개인키를 이용해 bandit14 계정으로 접속한 뒤에는 해당 파일을 읽을 권한이 생기므로, 먼저 현재 레벨의 비밀번호를 확인하였다.



```
cat /etc/bandit_pass/bandit14
```

![](/assets/img/posts/tistory/tistory-28-27.png)



이번 문제를 풀기 위해선 특정 호스트와 포트에 연결해서 데이터를 주고받는 도구인 nc(netcat)에 대해서 알아야 했는데, localhost의 30000번 포트에 현재 레벨의 비밀번호를 보내야 하므로, 다음과 같이 명령어를 입력하였다.



```
nc localhost 30000

#localhost = 현재 접속 중인 Bandit 서버 자기 자신
#30000 = 비밀번호를 제출해야 하는 포트 번호
```



이 명령어를 사용하게 되면 다음과 같이 입력을 기다리는 상태가 되는데 그때 앞에서 확인한 현재 레벨의 비밀번호를 입력하면 서버가 이를 확인하고, 다음 레벨의 비밀번호를 응답으로 출력하게된다.



![](/assets/img/posts/tistory/tistory-28-28.png)



비밀번호: 8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo



##  Level 15 → Level 16



목표: 현재 레벨의 비밀번호를 localhost의 30001번 포트로 제출하되, SSL/TLS 암호화 연결을 사용하여 다음 레벨의 비밀번호를 획득



현재 비밀번호는 8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo로 이미 앞선 단계에서 얻어놨다.



이번 문제에서는 nc 대신 SSL/TLS가 적용된 서버에 접속해서 데이터를 주고받을 수 있게 해주는 명령어인 openssl s_client를 이용해야 하는데,



```
openssl s_client -connect localhost:30001
```



다음과 같은 명령어로 이용할 수가 있다.



각각의 의미를 해석해보면 다음과 같다.

<table>
  <tbody>
    <tr>
      <td>openssl</td>
      <td>SSL/TLS 관련 기능을 제공하는 명령어</td>
    </tr>
    <tr>
      <td>s_client</td>
      <td>SSL/TLS 서버에 클라이언트처럼 접속하는 기능</td>
    </tr>
    <tr>
      <td>-connect</td>
      <td>접속할 대상 서버와 포트를 지정</td>
    </tr>
    <tr>
      <td>localhost:30001</td>
      <td>현재 서버의 30001번 포트에 접속</td>
    </tr>
  </tbody>
</table>





앞선 문제와 같이, 입력 대기를 기다리는 상태에서 현재 비밀번호를 입력해주면 다음 문제의 비밀번호가 나오게 된다.

![](/assets/img/posts/tistory/tistory-28-29.png)



비밀번호: kSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx





## Level 16 → Level 17



목표: 현재 레벨의 비밀번호를 localhost의 31000~32000 범위 안에 있는 포트 중 하나에 제출하여, 다음 레벨 접속 정보를 획득



이번 문제는 적혀있는 그대로, 31000~32000 포트 중 실제로 서버가 열려 있는 포트를 찾고, 그중 SSL/TLS 통신을 사용하는 포트를 찾은 후, 현재 비밀번호를 보냈을 때 다음 인증 정보를 돌려주는 포트를 찾아야 한다.



포트 범위를 알아내는 과정에서 nmap이라는 스캔 도구가 이용이 된다.

nmap은 특정 서버에서 어떤 포트가 열려 있는지 확인하는 포트 스캔 도구이다.



```
nmap -sV -p 31000-32000 localhost
#-sV: 열린 포트에서 동작하는 서비스의 종류/버전을 확인하는 옵션
```



이러한 구조로 이뤄지는데, 명령어를 해석하면 다음과 같다.





<table>
  <tbody>
    <tr>
      <td>nmap</td>
      <td>포트 스캔 도구</td>
    </tr>
    <tr>
      <td>-sV</td>
      <td>열린 포트의 서비스 정보를 확인</td>
    </tr>
    <tr>
      <td>-p 31000-32000</td>
      <td>31000번부터 32000번까지 검사</td>
    </tr>
    <tr>
      <td>localhost</td>
      <td>현재 접속 중인 Bandit 서버 자기 자신</td>
    </tr>
  </tbody>
</table>



결과를 확인해보면,



![](/assets/img/posts/tistory/tistory-28-30.png)



여기서 echo는 보낸 값을 그대로 다시 돌려주는 서비스이기 때문에, 문제에서 나머지는 보낸 값을 그대로 돌려준다고 했으니, echo들은 정답이 아니다. 31518은 ssl/echo라서 SSL은 쓰지만, 결국 echo 서비스라 정답이 아닐 가능성이 크고,

남은 것은 31790/tcp open ssl/unknown이 된다. SSL/TLS를 사용하지만 echo 서비스는 아닌 포트가 하나 뿐이기 때문.



```
openssl s_client -quiet -connect localhost:31790

#-quiet: 연결 과정에서 나오는 불필요한 출력이나 일부 안내 메시지를 줄이는 옵션
#-connect: 접속할 대상 서버와 포트를 지정하는 옵션
```

다음으로, 앞선 문제에서 배웠던 openssl s_client를 이용하여 서버에 접속하면 입력 대기가 뜨게 되고, 그곳에 현재 비밀번호를 입력한다.



![](/assets/img/posts/tistory/tistory-28-31.png)



Level 13 -> 14 때처럼 SSH 개인키가 나오기 때문에, 이전과 똑같은 방식으로 풀이를 진행.



```
exit
nano ~/bandit17.key #키 파일 생성
chmod 600 ~/bandit17.key
ssh -i ~/bandit17.key -p 2220 bandit17@bandit.labs.overthewire.org
```



![](/assets/img/posts/tistory/tistory-28-32.png)







## Level 17 → Level 18



목표: 홈 디렉토리에 passwords.old와 passwords.new 두 파일이 있고, 두 파일 사이에서 변경된 유일한 줄이 다음 레벨의 비밀번호. 두 파일의 차이 비교.



![](/assets/img/posts/tistory/tistory-28-33.png)

ls를 통해 파일을 확인하면 두개의 파일이 보인다.



이때, diff라는 두 파일의 차이점을 비교해서 보여주는 명령어를 사용하면 되는데

```
diff passwords.old passwords.new
```



다음과 같이 사용하면 된다.

<table>
  <tbody>
    <tr>
      <td>diff</td>
      <td>두 파일의 차이점을 비교하는 명령어</td>
    </tr>
    <tr>
      <td>passwords.old</td>
      <td>비교 기준이 되는 이전 파일</td>
    </tr>
    <tr>
      <td>passwords.new</td>
      <td>변경된 내용이 들어 있는 새 파일</td>
    </tr>
  </tbody>
</table>



![](/assets/img/posts/tistory/tistory-28-34.png)



> 줄이 passwords.new의 변경된 줄을 의미하기 때문에, 비밀번호는 x2gLTTjFwMOhQ8oWNbMN362QKxfRqGlO이 된다.



## Level 18 → Level 19



목표: 다음 레벨의 비밀번호는 홈 디렉토리의 readme 파일에 저장되어 있다. 하지만 .bashrc 파일이 수정되어 있어서 SSH로 로그인하면 바로 로그아웃되는 것을 우회해야 한다.





![](/assets/img/posts/tistory/tistory-28-35.png)



비밀번호를 치자마자 나가지는 것이 보인다. 정상 로그인해서 명령어를 입력하는 방식이 막혀 있으니, SSH 접속과 동시에 명령어를 실행하는 방법을 사용해야 한다.



SSH는 단순히 로그인만 하는 게 아니라, 접속하면서 원격 명령어를 바로 실행할 수가 있고, 문제에서 비밀번호가 readme 파일에 있다고 했으니까, 접속하면서 바로 cat readme를 실행하면 된다.



```
ssh -p 2220 bandit18@bandit.labs.overthewire.org cat readme
```



실행해보면 다음과 같이 password가 뜨는 것을 볼 수가 있다.

![](/assets/img/posts/tistory/tistory-28-36.png)



비밀번호: cGWpMaKXVwDUNgPAVJbWYuGHVn9zl3j8



## Level 19 → Level 20

다음 레벨에 접근하기 위해 홈 디렉토리에 있는 setuid binary를 사용해야 한다.
이 파일을 인자 없이 실행하면 사용 방법을 알 수 있고, setuid binary를 사용한 뒤 /etc/bandit_pass에서 이번 레벨의 비밀번호를 확인할 수 있다.



```
ls -l
```

우선 ls-l 를 사용해 파일을 자세히 봐본다.



![](/assets/img/posts/tistory/tistory-28-37.png)



bandit20-do 실행 파일이 보이는데, 문제에서 인자 없이 실행해보라고 했으니



```
./bandit20-do
```



우선 실행을 해본다.

![](/assets/img/posts/tistory/tistory-28-38.png)



Example: ./bandit20-do id라며 사용법이 출력되게 되는데, 이 사용법을 토대로 실행할 명령어를 붙이면



```
./bandit20-do cat /etc/bandit_pass/bandit20
```



이런 명령어가 되고, 각각 해석해보면 다음과 같은 뜻을 가진다.

<table>
  <tbody>
    <tr>
      <td>setuid</td>
      <td>실행 파일을 파일 소유자의 권한으로 실행하게 하는 권한</td>
    </tr>
    <tr>
      <td>ls -l</td>
      <td>파일 권한과 소유자 정보를 자세히 확인</td>
    </tr>
    <tr>
      <td>./파일명</td>
      <td>현재 디렉토리의 실행 파일 실행</td>
    </tr>
    <tr>
      <td>/etc/bandit_pass/bandit20</td>
      <td>bandit20 비밀번호 파일 위치</td>
    </tr>
  </tbody>
</table>



setuid가 걸린 실행 파일을 이용해 bandit20 권한으로 명령을 실행하고, 다음 레벨 비밀번호 파일을 읽게 되는 것이다.



![](/assets/img/posts/tistory/tistory-28-39.png)

비밀번호는 0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO이 된다.



## Level 20 → Level 21

목표: 홈 디렉토리에 있는 setuid binary는 사용자가 지정한 포트로 localhost에 연결한 뒤, 연결된 곳에서 한 줄의 텍스트를 읽고, 그것이 현재 레벨인 bandit20의 비밀번호와 일치하면 다음 레벨인 bandit21의 비밀번호를 전송.



문제를 요약해보면 먼저 서버 역할을 하는 포트를 열어두고, setuid binary가 그 포트로 접속하게 만들면 되는 것인데, 이전 문제들은 어떤 서버에 접속해서 비밀번호를 보내는 방식이었지만, 이번 문제는 반대로 네트워크 연결을 기다리는 쪽과 접속하는 쪽을 직접 구성해야한다.



![](/assets/img/posts/tistory/tistory-28-40.png)



우선 ls -l을 이용해서 파일을 보고 이번에는 nc를 서버처럼 사용하도록 명령어를 구성해야 한다.



```
echo "0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO" | nc -l -p 12345 &

#nc -l -p 12345는 해당 포트에서 연결을 기다리는 서버처럼 동작하게 됨
```

다음과 같은 명령어가 되는데, 각 부분의 의미는 다음과 같다



<table>
  <tbody>
    <tr>
      <td>echo "비밀번호"</td>
      <td>현재 비밀번호를 출력</td>
    </tr>
    <tr>
      <td>nc -l -p 12345</td>
      <td>12345번 포트에서 연결을 기다림</td>
    </tr>
    <tr>
      <td>&amp;</td>
      <td>이 명령어를 백그라운드에서 실행</td>
    </tr>
  </tbody>
</table>





실행한 후 바로 ./suconnect 12345를 통해 실행을 해주면, suconnect가 localhost:12345로 접속해서 nc가 보내는 비밀번호를 읽고, 맞으면 bandit21 비밀번호를 출력하게 된다.



![](/assets/img/posts/tistory/tistory-28-41.png)



비밀번호: EeoULMCra2q0dSkYj561DX7s1CpBuOBt



##  Level 21 → Level 22



목표: cron이라는 시간 기반 작업 스케줄러에 의해 어떤 프로그램이 주기적으로 자동 실행되고 있다. /etc/cron.d/ 디렉토리에서 설정 파일을 확인하고, 어떤 명령어가 실행되는지 알아내기.



우선

```
ls /etc/cron.d/
```

명령어를 통해 파일을 확인해본다.



![](/assets/img/posts/tistory/tistory-28-42.png)



bandit22와 관련된 cron 설정 파일을 찾아야 하는데, 파일을 살펴보면 cronjob_bandit22이라는 파일이 보인다.



```
cat /etc/cron.d/cronjob_bandit22
```

다음과 같은 명령어를 통해 확인해보면



![](/assets/img/posts/tistory/tistory-28-43.png)



설정 파일을 볼 수 있는데, 여기서 * * * * *는 실행 주기를 의미하고, bandit22 /usr/bin/cronjob_bandit22.sh는 bandit22 사용자 권한으로 /usr/bin/cronjob_bandit22.sh 스크립트를 실행한다는 뜻이다.



스크립트 경로를 찾았기 때문에, cat을 통해 한번 더 읽어서 확인을 해본다.

![](/assets/img/posts/tistory/tistory-28-44.png)



cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv은

 bandit22 비밀번호를 읽어서 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv에 저장한다는 뜻이기 때문에



```
cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

cat을 통해 파일을 확인 해주면



![](/assets/img/posts/tistory/tistory-28-45.png)



다음과 같이 비밀번호 tRae0UfB9v0UzbCdn9cY0gQnds9GF58Q가 나온다.



##  Level 22 → Level 23

목표: 이번에도 cron에 의해 어떤 프로그램이 주기적으로 자동 실행되고 있다. /etc/cron.d/ 디렉토리에서 설정 파일을 확인하고, 실제로 어떤 명령어가 실행되는지 분석.



이번에는 한 단계 더 나아가서, 단순히 스크립트를 따라가는 것뿐만 아니라 스크립트가 어떤 파일 이름을 만들고, 어디에 비밀번호를 저장하는지 이해해야 하는 문제이다. 문제에서 다른 사람이 작성한 shell script를 읽는 것은 매우 유용한 능력이라고 하고 있기 때문에, 이번 문제의 핵심은 쉘 스크립트를 읽고 동작을 해석하기가 된다.



```
ls /etc/cron.d/
```

ls를 통해서 bandit23과 관련된 파일을 찾고



![](/assets/img/posts/tistory/tistory-28-46.png)





cronjob_bandit23파일을 확인 후



```
cat /etc/cron.d/cronjob_bandit23
```



이전 문제처럼 cat을 통해 실제로 실행되는 스크립트 경로를 확인한다.

![](/assets/img/posts/tistory/tistory-28-47.png)



이전 문제에서 말했듯 * * * * *는 실행 주기를 의미하기 때문에, 매분 bandit23 사용자 권한으로 /usr/bin/cronjob_bandit23.sh를 실행한다는 뜻이 된다.



```
cat /usr/bin/cronjob_bandit23.sh
```



스크립트 내용을 확인해보면

![](/assets/img/posts/tistory/tistory-28-48.png)

다음과 같은 내용이 들어있는데, 각각의 의미를 해석해보면 다음과 같다.



<table>
  <tbody>
    <tr>
      <td>#!/bin/bash</td>
      <td>이 파일이 bash 쉘로 실행되는 스크립트임을 의미한다.</td>
    </tr>
    <tr>
      <td>myname=$(whoami)</td>
      <td>현재 스크립트를 실행하는 사용자 이름을 myname 변수에 저장한다. cron 설정에서 이 스크립트는 bandit23 권한으로 실행되므로, myname에는 bandit23이 들어간다.</td>
    </tr>
    <tr>
      <td>mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)</td>
      <td>I am user bandit23이라는 문자열을 만들고, 이를 MD5 해시값으로 변환한 뒤, 해시값 부분만 잘라 mytarget 변수에 저장한다.</td>
    </tr>
    <tr>
      <td>echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"</td>
      <td>어떤 비밀번호 파일을 어디로 복사하는지 안내 메시지를 출력한다.</td>
    </tr>
    <tr>
      <td>cat /etc/bandit_pass/$myname &gt; /tmp/$mytarget</td>
      <td>/etc/bandit_pass/bandit23 파일의 내용을 /tmp/해시값 파일로 저장한다. 즉, 이 파일 안에 다음 레벨 비밀번호가 들어 있다.</td>
    </tr>
  </tbody>
</table>



이어서 생각해보면, 이 스크립트는 실행 사용자의 이름을 기준으로 해시값을 생성하고, 해당 해시값을 파일명으로 사용하여 /tmp 디렉토리에 비밀번호 파일 내용을 저장한다. cron에 의해 bandit23 권한으로 실행되므로, 결과적으로 /etc/bandit_pass/bandit23의 내용이 /tmp/$mytarget에 저장된다는 뜻이다.





그 다음 스크립트에서 쓰는 해시값을 직접 계산해야 하는데

```
echo I am user bandit23 | md5sum | cut -d ' ' -f 1
```

다음과 같은 명령어를 통해 계산해볼 수가 있다.



각 부분은 다음과 같은 의미를 가진다



<table>
  <tbody>
    <tr>
      <td>echo I am user bandit23</td>
      <td>해시 계산에 사용할 문자열 출력</td>
    </tr>
    <tr>
      <td>md5sum</td>
      <td>입력 문자열의 MD5 해시값 계산</td>
    </tr>
    <tr>
      <td>cut -d ' ' -f 1</td>
      <td>공백 기준으로 첫 번째 값, 즉 해시값만 추출</td>
    </tr>
    <tr>
      <td>/tmp/해시값</td>
      <td>cron 스크립트가 비밀번호를 저장하는 파일 경로</td>
    </tr>
    <tr>
      <td>cat /tmp/해시값</td>
      <td>해당 파일 내용을 출력</td>
    </tr>
  </tbody>
</table>



계산으로 나온 해시값을 확인한 이후

![](/assets/img/posts/tistory/tistory-28-49.png)



```
cat /tmp/8ca319486bfbbc3663ea0fbe81326349
```

다음과 같은 명령어를 수행해주면



![](/assets/img/posts/tistory/tistory-28-50.png)



다음 레벨의 비밀번호인 0Zf11ioIjMVN551jX3CmStKLYqjk54Ga가 나오게 된다.



## Level 23 → Level 24



이번에도 cron에 의해 어떤 프로그램이 주기적으로 자동 실행되고 있다.
/etc/cron.d/에서 cron 설정을 확인하고, 실제로 어떤 명령어가 실행되는지 분석해야 한다.
이번 레벨에서는 직접 shell script를 만들어야 하며, 실행된 스크립트는 삭제될 수 있으므로 복사본을 따로 보관하는 것이 좋다는 것이 문제의 설명이다.



```
ls /etc/cron.d/
cat /etc/cron.d/cronjob_bandit24
```



다음과 같은 명령어를 통해 cron이 실제로 어떤 스크립트를 실행하는지 살펴본다.



![](/assets/img/posts/tistory/tistory-28-51.png)



```
cat /usr/bin/cronjob_bandit24.sh
```

명령어를 통해서 cron이 실행하는 스크립트 확인해보면,



![](/assets/img/posts/tistory/tistory-28-52.png)



다음과 같은 스크립트가 실행중임을 알 수가 있고, 이 스크립트는 `/var/spool/bandit24/foo` 안에 있는 파일들을 자동으로 실행하고 삭제한다. 다만 아무 파일이나 실행하는 것이 아니라, 소유자가 `bandit23`인 일반 파일만 실행한다. 따라서 bandit23 사용자인 내가 만든 스크립트를 이 디렉토리에 넣으면 cron이 주기적으로 실행해줄 수 있다.



스크립트의 내용을 하나씩 뜯어보면 다음과 같다.



<table>
  <tbody>
    <tr>
      <td>myname=$(whoami)</td>
      <td>현재 스크립트를 실행하는 사용자 이름을 저장</td>
    </tr>
    <tr>
      <td>cd /var/spool/"$myname"/foo</td>
      <td>/var/spool/bandit24/foo 디렉토리로 이동</td>
    </tr>
    <tr>
      <td>for i in * .*</td>
      <td>디렉토리 안의 일반 파일과 숨김 파일을 순회</td>
    </tr>
    <tr>
      <td>owner="$(stat --format "%U" ./$i)"</td>
      <td>각 파일의 소유자 확인</td>
    </tr>
    <tr>
      <td>[ "${owner}" = "bandit23" ] &amp;&amp; [ -f "$i" ]</td>
      <td>소유자가 bandit23이고 일반 파일인지 검사</td>
    </tr>
    <tr>
      <td>timeout -s 9 60 "./$i"</td>
      <td>조건을 만족하면 파일을 최대 60초 동안 실행</td>
    </tr>
    <tr>
      <td>rm -rf "./$i"</td>
      <td>실행 후 파일 삭제</td>
    </tr>
  </tbody>
</table>





bandit24 비밀번호를 직접 읽을 권한이 없는 상황이지만, cron은 bandit24 권한으로 실행될 가능성이 높기 때문에 직접 만든 스크립트 안에

```
cat /etc/bandit_pass/bandit24 > /tmp/내파일
```



처럼 적어두면, cron이 bandit24 권한으로 실행하면서 비밀번호를 /tmp/내파일에 저장해줄 수 있게 된다.



```
mktemp -d
```



명령어를 사용하게 되면 나의 작업 파일이 생기고,

![](/assets/img/posts/tistory/tistory-28-53.png)





```
cd /tmp/tmp.3h9KF69UC2
```



cd를 통해 나의 작업 파일으로 이동 후



```
touch result.txt #결과를 저장할 빈 파일 생성
chmod 666 result.txt #cron이 실행하는 bandit24 사용자도 이 파일에 쓸 수 있게 권한 설정
```



결과물을 받을 파일을 만든다.



```
nano script.sh
#nano를 통해 열어서

#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/tmp.3h9KF69UC2/result.txt

#다음과 같은 내용을 넣는다
```





![](/assets/img/posts/tistory/tistory-28-54.png)





이 때, 파일에 실행 권한을 부여하는 명령어인  chmod을 사용해야 한다. cron이 shell script를 실행하려면, 그 파일이 실행 가능한 상태여야 하기 때문이다.



```
chmod +x script.sh
```



다음 명령어를 통해 실행 권한을 준 뒤,



```
cp script.sh /var/spool/bandit24/foo/
```

cp를 통해 cron이 실행하는 폴더로 복사하면 된다.



![](/assets/img/posts/tistory/tistory-28-55.png)



그 이후 cat명령어를 사용해 봐보면 다음과 같은 비밀번호가 뜬다



비밀번호: gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8



## Level 24 → Level 25



30002번 포트에서 데몬이 실행 중이며, bandit24 비밀번호와 4자리 숫자 PIN을 함께 보내면 bandit25 비밀번호를 얻을 수 있는 문제이다. PIN은 직접 알아낼 수 없고, 0000부터 9999까지 모든 조합을 시도하는 brute-forcing 방식으로 찾아야 한다.



4자리 PIN을 자동으로 전부 대입해보는 문제이지만, 직접 하나 하나 치면 너무너무 오래 걸리게 된다. 반복문을 사용한 스크립트를 만들어야 하는데, 문제에서 말한 brute-forcing은 가능한 모든 경우의 수를 하나씩 시도하는 방식이라

4자리 숫자 PIN은 0000부터 9999까지 총 10,000개 경우가 있다.



```
mktemp -d
cd /tmp/tmp.MFrtARLWW9
```



우선 출력이 많을 수 있으니까 /tmp에 작업 디렉토리를 만들고 이동.



브루트포싱 스크립트 생성해야 하기 때문에

```
nano bforce.sh
```

nano를 통해 생성한다.



```
#!/bin/bash

PASSWORD=$(cat /etc/bandit_pass/bandit24)

for pin in {0000..9999}
do
    echo "$PASSWORD $pin"
done | nc localhost 30002 > result.txt
```



스크립트의 내용은 다음과 같이 작성하였는데, 각각 명령어를 해석해보면 다음과 같다.



<table>
  <tbody>
    <tr>
      <td>#!/bin/bash</td>
      <td>이 파일을 bash 쉘로 실행하겠다는 의미이다.</td>
    </tr>
    <tr>
      <td>PASSWORD=$(cat /etc/bandit_pass/bandit24)</td>
      <td>현재 레벨인 bandit24의 비밀번호를 읽어 PASSWORD 변수에 저장한다.</td>
    </tr>
    <tr>
      <td>for pin in {0000..9999}</td>
      <td>0000부터 9999까지의 모든 4자리 PIN을 하나씩 대입하며 반복한다.</td>
    </tr>
    <tr>
      <td>do ... done</td>
      <td>반복문에서 실행할 명령어 범위를 나타낸다.</td>
    </tr>
    <tr>
      <td>echo "$PASSWORD $pin"</td>
      <td>bandit24비밀번호 PIN 형태의 문자열을 출력한다.</td>
    </tr>
    <tr>
      <td>| nc localhost 30002</td>
      <td>반복문에서 만들어진 입력값들을 localhost의 30002번 포트로 전송한다.</td>
    </tr>
    <tr>
      <td>&gt; result.txt</td>
      <td>서버에서 돌아오는 응답을 화면에 출력하지 않고 result.txt 파일에 저장한다.</td>
    </tr>
  </tbody>
</table>





문제에서 매번 새 연결을 만들 필요는 없다고 했기 때문에, nc 연결을 반복해서 10000번 만드는 대신, 반복문에서 생성한 입력값 전체를 한 번에 nc localhost 30002로 전달하였다.

![](/assets/img/posts/tistory/tistory-28-56.png)



```
chmod +x bforce.sh
./bforce.sh
```

chmod를 통해 권한을 부여하고, ./bforce.sh로 현재 디렉토리에 있는 bforce.sh 파일을 실행.



대부분의 잘못된 PIN에 대해서는 서버가 Wrong!과 같은 실패 메시지를 반환하기 때문에,

```
grep -v "Wrong" result.txt
```

grep -v "Wrong"을 사용하여 Wrong이 포함된 줄을 제외하고 출력해보면



![](/assets/img/posts/tistory/tistory-28-57.png)



다음과 같은 비밀번호 iCi86ttT4KSNe1armKiwbQNmB3YJP3q4가 나오는 것을 볼 수가 있다.
