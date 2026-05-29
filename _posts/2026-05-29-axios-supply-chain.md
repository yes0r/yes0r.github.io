---
title: "Axios npm 공급망 공격 사고 분석"
date: 2026-05-29 09:00:00 +0900
categories: ["블로그/기술문서"]
render_with_liquid: false
---
2026년 3월 31일에 발생한 Axios npm 패키지 침해 사건을 정리한다. 공격이 어떤 순서로 진행됐고, 어떤 기법이 쓰였고, 원인과 대응 과정에서 부족했던 점이 무엇인지 살펴본다.

## 01 사건 개요

Axios는 자바스크립트에서 HTTP 요청을 보낼 때 가장 많이 쓰이는 라이브러리 중 하나다. 프론트엔드, 백엔드, CI/CD 빌드 파이프라인 등 거의 모든 곳에 의존성으로 들어가 있고, 주간 다운로드 수가 약 1억 회 정도 된다.[1]

2026년 3월 31일, 이 패키지의 수석 메인테이너 계정이 탈취되어 악성 버전 두 개(`axios@1.14.1`, `axios@0.30.4`)가 npm에 올라갔다. 두 버전은 `plain-crypto-js`라는 의존성을 끌어왔고, 이 의존성이 설치되는 시점에 macOS·Windows·Linux 모두에 RAT을 설치했다.[2]

여기서 RAT (Remote Access Trojan)란? 공격자가 감염된 기기를 원격에서 제어할 수 있게 하는 악성코드. 명령 실행, 파일 탈취, 추가 페이로드 다운로드 등이 가능하다.

Axios의 소스 코드 자체는 바뀌지 않았고,  메인테이너 계정이 탈취되어, 정상 코드에 악성 의존성만 추가되는 형태로 침해가 일어났다. 코드를 봐서는 정상인데 설치하면 감염되는 공급망 공격의 전형적인 사례라고 한다.

피해 규모가 컸던 이유 중 하나는 공격자가 두 개의 dist-tag를 모두 오염시켰다는 점이다. `1.14.1`은 `latest`로, `0.30.4`는 `legacy`로 태깅했다. 그래서 `npm install axios`로 새로 설치한 사용자와 구버전 API를 쓰던 사용자가 모두 악성 버전을 받게 됐다.[2]

---

## 02 공격 사전 준비 단계

### 2-1. 계정을 먼저 노리지 않았다

공격은 3월 31일보다 약 2주 전부터 시작됐다. 공격자는 npm 계정을 직접 뚫는 대신, 메인테이너 Jason Saayman을 대상으로 소셜 엔지니어링을 진행해 그의 PC에 RAT을 먼저 설치했다. 그리고 이 RAT을 통해 npm 계정 자격증명을 확보했다.[3]


왜 pc였을까? npm 계정 자체는 2FA로 보호돼 있을 가능성이 높기 때문이다. 하지만 개발자 PC를 장악하면 `~/.npmrc`에 평문으로 저장된 토큰이나 세션 정보를 그대로 가져갈 수 있다. 계정의 보호 장치를 우회하는 대신, 이미 인증된 환경을 통째로 확보한 것이다.

### 2-2. 미끼 버전을 먼저 올렸다

실제 악성 패키지를 올리기 전에, 공격자는 먼저 정상적으로 동작하는 미끼 버전을 배포했다. 3월 30일 05:57 UTC에 무해한 `plain-crypto-js@4.2.0`을 올려 레지스트리에 정상 기록을 남겨두고, 같은 날 23:59 UTC에 악성 `postinstall` 훅이 들어간 `plain-crypto-js@4.2.1`을 올렸다.[2]

Axios 악성 버전을 올리기 약 18시간 전에 의존성 패키지를 미리 준비해둔 셈이다. 이렇게 하면 Axios가 올라가는 즉시 동작이 가능하고, 갑자기 생긴 신규 패키지보다 의심을 덜 사게 된다.

---

## 03 악성 버전 배포

### 3-1. 배포 방식과 출처 증명의 변화

레지스트리 메타데이터만 봐도 침해 정황이 드러난다. 정상 릴리스에 항상 있던 메인테이너 이메일이 `jasonsaayman@gmail.com`에서 `ifstap@proton.me`로 바뀌었고, 배포 방식도 달라졌다.[2]

<table>

<thead>
<tr>
<th>버전</th>      <th>배포 이메일</th>      <th>배포 방식</th>      <th>SLSA 증명</th>
</tr>
</thead>

<tbody>

<tr>
<td><strong>1.14.0</strong> (정상)</td>      <td>gmail.com</td>      <td>GitHub Actions OIDC</td>      <td>있음</td>
</tr>

<tr>
<td><strong>1.14.1</strong> (악성)</td>      <td>proton.me</td>      <td>CLI 직접 퍼블리시</td>      <td>없음</td>
</tr>

<tr>
<td><strong>0.30.4</strong> (악성)</td>      <td>proton.me</td>      <td>CLI 직접 퍼블리시</td>      <td>없음</td>
</tr>

</tbody>

</table>

> **SLSA / OIDC 퍼블리시** — GitHub Actions의 신뢰된 워크플로우에서 단기 토큰(OIDC)으로 패키지를 배포하면, 해당 패키지가 어느 저장소의 어느 워크플로우에서 나왔는지 증명하는 출처 정보(provenance)가 자동으로 붙는다. 공격자는 이 방식 대신 로컬에서 `npm publish`를 직접 실행해 증명 없는 패키지를 올렸다.

정상적인 OIDC 플로우에서 이메일 변경과 CLI 직접 퍼블리시로 바뀐 것 자체가 무단 접근을 보여주는 신호였다.[2] 하지만 이 이상 징후를 실시간으로 차단하는 자동 장치가 없었다는 점이 문제였다.

---

## 04 페이로드 실행 과정

### 4-1. postinstall 훅으로 자동 실행

이 공격의 전달 과정은 npm의 `postinstall` 라이프사이클 훅에 의존한다. 악성 Axios를 설치하면 `plain-crypto-js@^4.2.1`이 의존성으로 끌려오는데, 이 패키지의 `package.json`에는 다음이 들어 있었다.[2]

```text
"scripts": {
"postinstall": "node setup.js"
}
```

이 설정 때문에 `npm install` 도중 `setup.js`가 사용자 동작 없이 자동으로 실행된다. 패키지를 직접 import 하지 않아도 설치하는 것만으로 코드가 실행되는 구조다.

### 4-2. 2단계 인코딩으로 난독화된 드로퍼

`setup.js`는 정적 분석을 피하기 위해 두 단계 인코딩을 사용했다.[2]

- **1단계:** 문자열 역전(reverse) 후 Base64 디코딩
- **2단계:** `OrDeR_7077` 키와 위치 기반 인덱스(`7 * i² % 10`)를 쓴 XOR 복호화

C2 URL, 셸 커맨드, 모듈명 같은 문자열을 인코딩된 배열 `stq[]`에 넣어두고 런타임에 복호화한다. 복호화 후에는 OS를 판별해 분기한다.

```text
os.platform() 확인
↓
POST http://sfrclak[.]com:8000/6202033
body: { product: "packages.npm.org/product0" } ← macOS
      "packages.npm.org/product1" ← Windows
      "packages.npm.org/product2" ← Linux
↓
C2가 OS별 Stage 2 RAT 페이로드 응답
↓
플랫폼별 방식으로 실행
```

**위장 기법**

C2 요청 본문의 `packages.npm.org/` 접두사는 의도적인 위장이다. 네트워크 로그에서 봤을 때 정상 npm 레지스트리 통신처럼 보이게 만들어 탐지를 어렵게 한다.

### 4-3. OS별 전달 방식

<table>

<thead>
<tr>
<th>OS</th>      <th>전달 방식</th>      <th>저장 위치 (위장)</th>
</tr>
</thead>

<tbody>

<tr>
<td><strong>macOS</strong></td>      <td>osascript(AppleScript)로 curl 실행</td>      <td><code>/Library/Caches/com.apple.act.mond</code><br>Apple 시스템 데몬으로 위장</td>
</tr>

<tr>
<td><strong>Windows</strong></td>      <td>VBScript로 .ps1 다운로드 후 이름 바꾼 PowerShell로 실행</td>      <td><code>%TEMP%\6202033.ps1</code><br>wt.exe = Windows Terminal로 위장</td>
</tr>

<tr>
<td><strong>Linux</strong></td>      <td>curl로 다운로드 후 python3 직접 실행</td>      <td><code>/tmp/ld.py</code></td>
</tr>

</tbody>

</table>

### 4-4. 안티 포렌식

드로퍼는 실행을 마치면 흔적을 지운다.[2]

- **자기 삭제:** `fs.unlink(__filename)`으로 `setup.js` 자신을 삭제한다.
- **매니페스트 교체:** `postinstall` 훅이 없는 깨끗한 버전을 `package.md`라는 이름으로 미리 넣어두고, 실행 후 악성 `package.json`을 이걸로 덮어쓴다.

그 결과 사후에 `node_modules/plain-crypto-js/package.json`을 확인해도 악성 훅 흔적이 남지 않는다. 증거로 남는 것은 lockfile과 npm audit 로그 정도다. 포렌식 관점에서 침해 범위를 확인하기 어렵게 만드는 부분이다.

---

## 05 Stage 2 RAT 분석

세 플랫폼의 페이로드는 각각 다른 언어(Windows = PowerShell, macOS = C++, Linux = Python)로 작성됐지만, 서로 다른 도구가 아니라 같은 RAT 명세를 세 언어로 구현한 것이다. C2 프로토콜, 커맨드 셋, 비콘 주기, User-Agent가 모두 동일했다. Elastic은 이를 하나의 설계 문서를 공유하는 개발자 또는 팀의 작업으로 분석했다.[2]

<table>

<thead>
<tr>
<th>항목</th>      <th>세 변종 공통 값</th>
</tr>
</thead>

<tbody>

<tr>
<td>C2 전송</td>      <td>HTTP POST</td>
</tr>

<tr>
<td>본문 인코딩</td>      <td>Base64 JSON</td>
</tr>

<tr>
<td>User-Agent</td>      <td><code>mozilla/4.0 (compatible; msie 8.0; windows nt 5.1; trident/4.0)</code></td>
</tr>

<tr>
<td>비콘 주기</td>      <td>60초</td>
</tr>

<tr>
<td>세션 UID</td>      <td>실행마다 생성되는 16자 랜덤 문자열</td>
</tr>

</tbody>

</table>

**탐지 포인트**

스푸핑된 IE8 / Windows XP User-Agent가 세 OS 모두에서 동일하게 사용된다. 이 값은 시대착오적이기 때문에, macOS나 Linux 호스트에서 이 UA가 관측되면 그 자체로 강한 침해 지표(IoC)가 된다.

### 5-1. 초기화와 정찰

RAT은 실행 직후 세션 UID를 생성하고, OS와 아키텍처를 감지하고, 사용자 프로필·문서·데스크톱 등 관심 디렉터리를 열거한 뒤 `FirstInfo` 비콘을 C2로 전송한다. 이어지는 `BaseInfo` 하트비트에는 호스트명, 유저명, OS 버전, 타임존, 부팅 시각, 하드웨어 모델, CPU 타입, 전체 프로세스 목록이 포함된다.[2]

### 5-2. C2 커맨드 셋

세 변종 모두 동일한 네 가지 명령을 구현한다.[2]

- **kill** — 자기 종료. 단, Windows 변종의 지속성 메커니즘은 별도로 정리하지 않으면 남는다.
- **runscript** — 임의 스크립트/커맨드 실행. 공격자가 주로 쓰는 명령이다. Windows는 PowerShell, macOS는 AppleScript, Linux는 셸 또는 Python으로 실행한다.
- **peinject** — 바이너리 페이로드 드롭 및 실행. 이름은 Windows 중심이지만 세 OS 모두에서 추가 바이너리를 떨군다.
- **rundir** — 지정 경로의 디렉터리 열거.

이 RAT은 자격증명 탈취뿐 아니라 임의 코드 실행과 추가 페이로드 투하까지 가능하다. 개발자 PC나 CI 러너에서 실행되면 해당 환경의 자격증명과 시크릿이 모두 노출될 수 있다.

### 5-3. Shai-Hulud 계열에서 보이는 공격 방식

사용자가 알려준 `g00dfe11ow/Shai-Hulud-Open-Source` 저장소는 현재 GitHub Staff에 의해 비활성화되어 원본 코드를 직접 열람할 수는 없었다. 다만 이 저장소가 공개됐을 때의 분석 자료를 보면, Shai-Hulud 계열은 단순한 악성 패키지가 아니라 **스스로 퍼지는 공급망 웜**에 가깝다.[4]

핵심 흐름은 다음과 같다.

```text
유지보수자 계정 또는 CI/CD 환경 침해
↓
해당 계정이 관리하는 npm/PyPI 패키지에 악성 설치 스크립트 삽입
↓
사용자가 정상 패키지처럼 설치
↓
preinstall / postinstall / prepare 같은 라이프사이클 훅 실행
↓
토큰, 클라우드 키, GitHub/npm 자격증명 수집
↓
훔친 권한으로 새 저장소 생성 또는 기존 패키지 재배포
↓
다른 사용자와 패키지로 재확산
```

여기서 무서운 부분은 공격자가 취약한 서버 하나를 직접 때리는 게 아니라, **신뢰받는 개발 흐름 자체를 실행 경로로 쓴다**는 점이다. `npm install`은 개발자 입장에서는 평범한 설치 명령이지만, 패키지 안에 라이프사이클 스크립트가 있으면 설치 도중 코드가 자동으로 실행된다. 그래서 악성 코드가 애플리케이션 본문에 import 되지 않아도 이미 실행될 수 있다.

Shai-Hulud의 여러 파생 공격은 실행 훅을 계속 바꿨다. 초기에는 `postinstall`, 이후에는 `preinstall`, 최근 변종에서는 Git 기반 `optionalDependency`의 `prepare` 스크립트까지 사용했다.[4] `optionalDependency`는 설치 실패가 조용히 무시될 수 있기 때문에, 페이로드가 실행된 뒤 의존성 설치가 실패한 것처럼 보여도 사용자는 이상을 눈치채기 어렵다.

<table>

<thead>
<tr>
<th>단계</th>      <th>공격자가 노리는 것</th>      <th>왜 위험한가</th>
</tr>
</thead>

<tbody>

<tr>
<td>설치 훅 실행</td>      <td><code>preinstall</code>, <code>postinstall</code>, <code>prepare</code></td>      <td>패키지를 쓰기도 전에 코드가 먼저 실행된다.</td>
</tr>

<tr>
<td>자격증명 수집</td>      <td>GitHub, npm, AWS, GCP, K8s, SSH, CI secret</td>      <td>개발자 PC와 CI 러너는 배포 권한을 함께 들고 있는 경우가 많다.</td>
</tr>

<tr>
<td>GitHub 악용</td>      <td>새 저장소 생성, 브랜치 생성, 워크플로우 삽입</td>      <td>탈취한 토큰으로 피해자 계정 안에서 공격 흔적과 유출 데이터를 만든다.</td>
</tr>

<tr>
<td>재배포</td>      <td>피해자가 관리하는 패키지에 악성 코드 삽입</td>      <td>다음 설치자가 다시 감염되며 웜처럼 퍼진다.</td>
</tr>

</tbody>

</table>

Microsoft 분석에서도 Shai-Hulud 2.0 계열은 Bun 런타임을 이용해 악성 스크립트를 실행하고, TruffleHog 같은 도구로 저장된 credential과 클라우드 자격증명을 찾으며, GitHub Actions Runner를 악용해 지속성을 확보하는 흐름이 확인됐다.[5] 즉 페이로드의 목적은 단순 감염이 아니라 “권한 있는 개발 환경을 장악하고, 그 권한으로 다음 패키지를 오염시키는 것”에 있다.

Axios 사건은 Shai-Hulud 전체 체인처럼 자동 전파 웜으로 확산된 사례는 아니지만, 공통점이 뚜렷하다. 둘 다 사용자가 신뢰하는 패키지 설치 과정을 이용했고, 설치 훅으로 사용자 동작 없이 코드를 실행했으며, 개발자/CI 환경의 자격증명을 주요 목표로 삼았다. 그래서 이 사건을 볼 때 단순히 “악성 버전이 3시간 올라갔다”가 아니라, 오픈소스 공급망에서 설치 스크립트 하나가 배포 권한까지 이어질 수 있다는 점을 봐야 한다.

---

## 06 탐지와 대응 타임라인

이 사건은 자동화된 보안 시스템이 아니라 커뮤니티가 먼저 발견했다는 점이 특징이다.[3]

<table>

<thead>
<tr>
<th>시간</th>      <th>내용</th>
</tr>
</thead>

<tbody>

<tr>
<td>3/30 05:57 UTC</td>      <td>plain-crypto-js@4.2.0 (미끼 버전) 배포 — 정상 기록 남기기용</td>
</tr>

<tr>
<td>3/30 23:59 UTC</td>      <td>plain-crypto-js@4.2.1 (악성 postinstall) 배포 — 18시간 전 사전 준비</td>
</tr>

<tr>
<td>3/31 00:21 UTC</td>      <td>axios@1.14.1 악성 버전 배포 — latest 태그, plain-crypto-js 주입</td>
</tr>

<tr>
<td>3/31 ~01:00 UTC</td>      <td>axios@0.30.4 악성 버전 배포 — legacy 태그까지 포함</td>
</tr>

<tr>
<td>3/31 ~01:00 UTC</td>      <td>커뮤니티가 침해를 발견해 GitHub 이슈 제기 → 공격자가 탈취 계정으로 이슈 삭제</td>
</tr>

<tr>
<td>3/31 01:38 UTC</td>      <td>협력자 DigitalBrainJS가 deprecate PR 제출, 삭제된 이슈를 커뮤니티에 알리고 npm에 직접 연락</td>
</tr>

<tr>
<td>3/31 01:50 UTC</td>      <td>Elastic Security Labs가 GitHub 보안 권고 제출, 공동 대응 조율</td>
</tr>

<tr>
<td>3/31 03:15 UTC</td>      <td>악성 axios 버전 npm에서 제거</td>
</tr>

<tr>
<td>3/31 03:29 UTC</td>      <td>plain-crypto-js 제거 → 총 노출 시간 약 3시간</td>
</tr>

</tbody>

</table>

> **메인테이너 대응**

메인테이너는 포스트모템에서 모든 디바이스 완전 초기화와 플랫폼 구분 없이 전 계정 자격증명 재설정을 진행했다고 밝혔다. 재발 방지책으로는 불변(immutable) 릴리스 설정, OIDC 퍼블리시 플로우의 제대로 된 도입, GitHub Actions 모범사례 적용을 제시했다.[3]

---

## 07 근본 원인

표면적으로는 계정 하나가 탈취된 사건이지만, 자세히 보면 여러 원인이 겹쳐 있다.

### 원인 1 — 메인테이너 개인 PC가 곧 배포 권한

다운로드 수가 많은 패키지의 배포 권한이 한 개인의 PC 보안에 의존하고 있었다. PC가 RAT에 감염되자 npm 배포 권한도 함께 넘어갔다. 메인테이너 본인도 포스트모템에서 개인 계정에서 직접 배포한 것 자체가 피할 수 있었던 위험이었다고 적었다.[3]

### 원인 2 — 무단 배포를 잡을 자동 탐지 부재

이메일 변경, SLSA 증명 누락, 비정상 CLI 퍼블리시처럼 명백한 신호가 여럿 있었지만, 이를 실시간으로 차단하는 장치가 없었다. 탐지는 전적으로 커뮤니티가 우연히 알아챈 것에 의존했다. 메인테이너도 무단 배포를 자동으로 감지할 방법이 없었다고 언급했다.[3]

### 원인 3 — 설치가 곧 코드 실행인 npm 구조

`postinstall` 훅은 정상 기능이지만, 패키지를 설치하는 것만으로 임의 코드가 실행되는 통로이기도 하다. 개발자가 코드를 검토할 기회 없이 감염될 수 있다.

### 원인 4 — 버전 고정 미흡

lockfile로 버전을 고정하지 않았거나, 영향 시간대(00:21~03:15 UTC)에 새로 설치를 진행한 환경이 피해를 입었다. 반대로 안전한 버전에 고정해두고 이 시간대에 fresh install을 하지 않은 곳은 영향을 받지 않았다.[3]

---

## 08 대응 방법과 미흡했던 점

### 8-1. 감염 여부 확인

메인테이너가 포스트모템에서 안내한 확인 방법은 다음과 같다.[3]

```text
# lockfile에서 악성 버전 흔적 검색
grep -E "axios@(1\.14\.1|0\.30\.4)|plain-crypto-js" \
package-lock.json yarn.lock 2>/dev/null
```

위 명령에 무언가 잡히면 그 기기는 침해된 것으로 간주하고 다음을 수행한다.

- `axios@1.14.0` (0.x는 `0.30.3`)으로 다운그레이드
- `node_modules/plain-crypto-js/` 삭제
- 해당 기기의 모든 시크릿·토큰·자격증명 교체
- 네트워크 로그에서 `sfrclak[.]com` / `142.11.206.73` 의 8000 포트 연결 확인
- CI 러너에서 발생했다면 해당 빌드에 주입된 모든 시크릿 교체

### 8-2. 잘 대응한 점

- **커뮤니티의 빠른 공조:** 자동 시스템이 잡지 못한 침해를 개발자들이 발견했고, 권한이 더 낮은 협력자가 npm에 직접 연락해 한 시간여 만에 deprecate를 이끌어냈다.
- **투명한 포스트모템:** 메인테이너가 타임라인과 원인, 재발 방지책을 공개해 다른 프로젝트도 참고할 수 있게 했다.
- **제3자 보안팀의 빠른 분석:** Elastic 등이 IoC와 탐지 규칙을 신속하게 공개해 방어 측이 대응할 수 있었다.

### 8-3. 미흡했던 점

- **사전 예방 실패:** OIDC 강제 퍼블리시와 불변 릴리스 설정은 사고 이후에야 도입됐다. 메인테이너 본인이 진작 있었어야 했다고 인정한 부분이다.
- **레지스트리 측 탐지 공백:** 이메일 변경과 증명 없는 CLI 배포라는 명백한 이상 징후를 npm이 자동으로 막지 못했다.
- **안티 포렌식 대응의 한계:** 페이로드가 자기삭제를 하기 때문에 lockfile 외에는 사후 증거가 거의 남지 않아, 피해 기관이 정확한 침해 범위를 파악하기 어려웠다.



① lockfile로 버전 고정, `^`·`~` 범위 지정 지양 / ② CI에서 `npm ci --ignore-scripts`로 라이프사이클 스크립트 차단 / ③ 퍼블리시는 OIDC·provenance 강제 / ④ 메인테이너 계정 MFA 필수 / ⑤ 새 버전은 일정 기간 cooldown 후 채택

---

## 09 정리

Axios 사건은 특별히 새로운 공격 기법이 등장한 게 아니라, 이미 알려진 약점들이 한꺼번에 맞물려서 일어났다. 메인테이너 PC 침해, `postinstall` 훅을 통한 자동 실행, 무단 배포에 대한 자동 탐지 부재가 겹치면서, 주간 1억 다운로드 규모의 라이브러리가 약 3시간 동안 악성 버전으로 배포됐다.

이 사례를 정리하면서 가장 기억에 남았던 건 `npm install` 한 줄이 곧 외부 코드를 실행시키는 행위라는 점이었다. 평소에 별 생각 없이 쓰는 명령이지만, 의존성 하나만 오염돼도 설치 시점에 바로 코드가 돌 수 있다는 걸 다시 확인했다.



---

## 참고 자료

- [Trend Micro — Axios NPM Package Compromised](https://www.trendmicro.com/en_us/research/26/c/axios-npm-package-compromised.html) — trendmicro.com
- [Elastic Security Labs — Inside the Axios supply chain compromise: one RAT to rule them all](https://www.elastic.co/security-labs/axios-one-rat-to-rule-them-all) — elastic.co/security-labs
- [Microsoft Security Blog — Shai-Hulud 2.0: Guidance for detecting, investigating, and defending against the supply chain attack](https://www.microsoft.com/en-us/security/blog/2025/12/09/shai-hulud-2-0-guidance-for-detecting-investigating-and-defending-against-the-supply-chain-attack/) — microsoft.com
