---
title: "IDS/IPS란 무엇인가?"
date: 2026-05-27 21:32:00 +0900
categories: ["블로그/기술문서"]
render_with_liquid: false
---
침입 탐지 및 차단 시스템의 개념, 동작 원리, 유형, 장단점과 실제 보안 운영 환경에서의 활용 방법을 정리한다.

## 1. IDS/IPS란 무엇인가?

네트워크 보안을 공부하다 보면 방화벽(Firewall) 다음으로 꼭 나오는 게 IDS와 IPS다. 방화벽이 허용/차단 규칙으로 트래픽을 걸러내는 문지기라면, IDS와 IPS는 그 안에서 일어나는 일을 들여다보는 감시 시스템에 가깝다.<br>

핵심을 먼저 정의해보자면 다음과 같다.<br>

**핵심 정의**<br>

**IDS (Intrusion Detection System)** — 침입 탐지 시스템. 네트워크나 시스템에서 의심스러운 활동을 탐지하고 관리자에게 알린다. 직접 차단하지는 않는다.

 **IPS (Intrusion Prevention System)** — 침입 차단 시스템. 탐지에서 한 발 더 나아가 의심스러운 트래픽을 실시간으로 차단한다.<br>

쉽게 비유하면 IDS는 CCTV, IPS는 자동 잠금 장치다. CCTV는 수상한 사람을 발견하면 경고음을 울리지만 직접 막지는 않는다. 자동 잠금 장치는 수상한 행동이 감지되면 문을 바로 잠가버린다.<br>

### 방화벽, WAF와 어떻게 다른가<br>

IDS/IPS를 처음 접하다보니 방화벽(Firewall)이나 WAF(Web Application Firewall)와 뭐가 다른 건지 헷갈리기 쉬웠다. 표로 비교하자면 다음과 같다.<br>

<table>

       <thead>

           <tr>
     <th>구분</th>      <th>방화벽 (Firewall)</th>      <th>WAF</th>      <th>IDS/IPS</th>
   </tr>

       </thead>

       <tbody>

           <tr>

               <td>판단 기준</td>
               <td>IP, 포트, 프로토콜, 방향</td>
               <td>복호화된 HTTP/HTTPS 요청 내용</td>
               <td>트래픽 내용 + 행위 패턴</td>

   </tr>

           <tr>

               <td>분석 계층</td>
               <td>3~4계층 (네트워크/전송)</td>
               <td>7계층 (애플리케이션, 웹 전용)</td>
               <td>3~7계층 전반</td>

   </tr>

           <tr>

               <td>탐지 대상</td>
               <td>비허가 IP/포트 접근</td>
               <td>SQL Injection, XSS 등 웹 공격</td>
               <td>네트워크/시스템 전반의 침입 행위</td>

   </tr>

           <tr>

               <td>차단 방식</td>
               <td>규칙 기반 허용/차단</td>
               <td>웹 요청 필터링</td>
               <td>시그니처/이상 행위/정책 기반</td>

   </tr>

       </tbody>

   </table>

전통적인 방화벽은 주로 "이 IP, 이 포트, 이 프로토콜을 허용/차단할 것인가"를 기준으로 동작한다. 허용된 포트로 들어오는 공격 트래픽은 방화벽이 막을 수 없다. WAF는 웹 애플리케이션 계층에 특화돼 있어서 HTTP 요청 내용을 분석하지만, 웹 이외의 프로토콜이나 네트워크 레벨 공격은 커버하지 못한다. IDS/IPS는 트래픽의 내용과 행위를 분석해서 방화벽과 WAF가 각각 놓칠 수 있는 공격을 잡아낸다. 그래서 세 가지가 서로 보완하는 관계로 함께 배치되는 경우가 많다.

## 2. IDS의 개념과 역할

IDS는 네트워크 트래픽이나 시스템 로그를 실시간으로 분석해서 알려진 공격 패턴이나 비정상적인 행동을 탐지한다. 탐지 결과는 관리자에게 경보(Alert) 형태로 전달되고, 관리자가 상황을 판단해서 대응 여부를 결정한다.

IDS가 모니터링하는 대상에 따라 두 가지로 나뉜다.

<table>

       <thead>

           <tr>
     <th>유형</th>      <th>풀네임</th>      <th>모니터링 대상</th>      <th>특징</th>
   </tr>

       </thead>

       <tbody>

           <tr>

               <td>NIDS</td>
               <td>Network-based IDS</td>
               <td>네트워크 트래픽 전체</td>
               <td>네트워크 구간에 설치, 패킷 단위 분석. 암호화된 트래픽은 분석 어려움</td>

   </tr>

           <tr>

               <td>HIDS</td>
               <td>Host-based IDS</td>
               <td>개별 호스트의 시스템 로그, 파일, 프로세스</td>
               <td>각 호스트에 에이전트 설치. 내부 행동까지 상세 모니터링 가능</td>

   </tr>

       </tbody>

   </table>

NIDS는 네트워크 전체를 한 번에 볼 수 있다는 게 장점이지만, 암호화된 트래픽(HTTPS 등)은 내용을 들여다볼 수 없어서 한계가 있다. HIDS는 각 서버마다 에이전트를 깔아야 해서 관리 부담이 있지만, 내부에서 일어나는 파일 변조나 권한 상승 같은 행동까지 잡아낼 수 있다.

IDS의 주요 역할을 정리하면 이렇다.

- 실시간 트래픽 및 로그 모니터링
- 알려진 공격 패턴과의 매칭 (시그니처 기반)
- 비정상적인 행동 패턴 탐지 (이상 행위 기반)
- 보안 이벤트 로그 수집 및 저장
- 관리자에게 경보 발송
- 포렌식 분석을 위한 증거 데이터 보존

## 3. IPS의 개념과 역할

IPS는 IDS에 차단 기능을 더한 시스템이다. 탐지만 하는 게 아니라 의심스러운 트래픽을 실시간으로 드롭(Drop)하거나, 연결을 강제로 종료하거나, 해당 IP를 블랙리스트에 올린다.

IDS가 네트워크 경로 밖에(Out-of-band) 위치해서 트래픽을 복사해서 분석하는 것과 달리, IPS는 트래픽이 실제로 통과하는 경로(Inline)에 위치한다. 트래픽이 IPS를 통과해야만 목적지에 도달할 수 있는 구조다.

| 흐름 | 뜻 |
| --- | --- |
| 외부 트래픽 → **IPS (Inline)** → 내부 네트워크 | 트래픽이 IPS를 통과해야 목적지에 도달하는 구조 |

이 구조 때문에 IPS는 즉각적인 차단이 가능하지만, 반대로 오탐(False Positive)이 발생하면 정상 트래픽도 차단해 버리는 위험이 있다. 그래서 IPS 운영에서 탐지 규칙 튜닝이 얼마나 잘 돼 있느냐가 굉장히 중요하다.

IPS의 주요 차단 방식:

- **패킷 드롭(Packet Drop)**: 악성으로 판단된 패킷을 그냥 버린다
- **세션 종료(Session Reset)**: TCP RST 패킷을 보내서 연결을 강제로 끊는다
- **IP 차단(IP Blocking)**: 공격 출발지 IP를 일정 시간 또는 영구적으로 차단한다
- **트래픽 제한(Rate Limiting)**: DDoS처럼 특정 IP에서 과도한 요청이 오면 속도를 제한한다

## 4. IDS와 IPS의 동작 원리

IDS/IPS가 어떻게 공격을 탐지하는지가 핵심이다. 대표적으로 시그니처 기반 탐지, 이상 행위 기반 탐지, 정책 기반 탐지, 상태 기반 프로토콜 분석 방식이 있다.<br>

### 4-1. 시그니처 기반 탐지 (Signature-based Detection)

가장 전통적인 방식이다. 악성코드나 공격 패턴을 데이터베이스에 저장해 두고, 들어오는 트래픽이 그 패턴과 일치하면 탐지한다. 바이러스 백신이 악성코드 해시를 비교하는 것과 같은 원리다.<br>

| 단계 | 하는 일 |
| --- | --- |
| 1 | 트래픽/로그 수집 |
| 2 | 패턴 추출 |
| 3 | 시그니처 DB와 비교 |
| 4 | 일치 시 탐지/차단 |

시그니처 예시를 들면, SQL Injection 공격에서 자주 쓰이는 `' OR '1'='1` 같은 문자열이나, Shellshock 취약점 공격에 쓰이는 특정 HTTP 헤더 패턴을 시그니처로 등록해 두는 식이다.<br>

<table>

       <thead>

           <tr>
     <th>장점</th>      <th>단점</th>
   </tr>

       </thead>

       <tbody>

           <tr>

               <td>알려진 공격에 대한 탐지 정확도가 높음</td>
               <td>알려지지 않은 공격(제로데이)은 탐지 불가</td>

   </tr>

           <tr>

               <td>오탐률(False Positive)이 낮음</td>
               <td>시그니처 DB를 지속적으로 업데이트해야 함</td>

   </tr>

           <tr>

               <td>처리 속도가 빠름</td>
               <td>공격자가 패턴을 조금만 변형하면 우회 가능</td>

   </tr>

       </tbody>

   </table>

### 4-2. 이상 행위 기반 탐지 (Anomaly-based Detection)

정상적인 네트워크 트래픽이나 시스템 동작의 기준선(Baseline)을 학습해 두고, 그 기준에서 크게 벗어나는 행동을 탐지하는 방식이다. 머신러닝이나 통계 기법이 많이 활용된다.<br>

예를 들어 평소에 특정 서버로 하루에 1,000개 정도의 요청이 들어온다면, 갑자기 100,000개가 들어올 경우 DDoS 공격이나 비정상 트래픽으로 판단하는 식이다.<br>

시그니처 기반과 달리 알려지지 않은 새로운 공격도 탐지할 수 있다는 게 핵심 장점이다. 하지만 정상의 기준을 정의하는 게 어렵고, 정상 트래픽도 비정상으로 잡히는 오탐이 상대적으로 많다. 특히 운영 환경이 자주 바뀌거나 이벤트성 트래픽이 많은 경우에는 기준선 유지 자체가 힘들다.<br>

<table>

       <thead>

           <tr>
     <th>장점</th>      <th>단점</th>
   </tr>

       </thead>

       <tbody>

           <tr>

               <td>제로데이 공격 탐지 가능</td>
               <td>오탐률이 높음</td>

   </tr>

           <tr>

               <td>내부자 위협, APT 같은 복잡한 공격도 탐지 가능</td>
               <td>기준선 학습에 시간 필요</td>

   </tr>

           <tr>

               <td>시그니처 업데이트 불필요</td>
               <td>환경 변화에 민감하게 반응해 오탐 증가 가능</td>

   </tr>

       </tbody>

   </table><br>

### 4-3. 정책 기반 탐지 (Policy-based Detection)

조직이 정의한 보안 정책을 기준으로 탐지하는 방식이다. 시그니처나 통계적 이상 행동이 아니라, '이런 행동은 허용하지 않는다'는 명시적 규칙을 기반으로 한다.

예를 들어 "업무 시간 외(오후 11시~오전 7시)에 외부에서 내부 데이터베이스 서버로의 접근은 모두 탐지한다'거나, '특정 내부 서버에서 외부로 나가는 FTP 트래픽은 허용하지 않는다' 같은 식으로 규칙을 정의한다.<br>

시그니처 기반보다 유연하게 조직의 상황에 맞게 규칙을 짤 수 있다. 다만 규칙을 만드는 사람이 공격 유형과 자사 환경을 잘 이해하고 있어야 하고, 환경이 바뀔 때마다 정책도 업데이트해야 한다.<br>

### 4-4. 상태 기반 프로토콜 분석 (Stateful Protocol Analysis)

프로토콜이 정상적으로 동작하는 흐름을 사전에 정의해 두고, 그 흐름에서 벗어나는 트래픽을 탐지하는 방식이다. NIST SP 800-94에서도 IDS/IPS의 핵심 탐지 방식 중 하나로 분류한다.<br>

예를 들어 HTTP 프로토콜에서는 클라이언트가 먼저 요청을 보내고 서버가 응답하는 순서가 정해져 있다. 이 순서를 거스르거나, 헤더 형식이 HTTP 명세를 벗어나거나, DNS 요청 하나에 비정상적으로 긴 쿼리가 담겨 있다면 프로토콜 분석으로 탐지할 수 있다.<br>

시그니처 기반이 알려진 나쁜 것을 찾는 방식이라면, 상태 기반 프로토콜 분석은 정상 프로토콜 규격에서 벗어난 것을 찾는 방식이다. 제로데이 공격이나 프로토콜 터널링(DNS 터널링, ICMP 터널링 등)을 탐지하는 데 특히 유용하다.<br>

<table>

       <thead>

           <tr>
     <th>장점</th>      <th>단점</th>
   </tr>

       </thead>

       <tbody>

           <tr>

               <td>프로토콜 규격 위반 공격 탐지 가능</td>
               <td>프로토콜별 정상 상태 정의가 복잡함</td>

   </tr>

           <tr>

               <td>시그니처 없이도 비정상 행동 탐지</td>
               <td>독점 프로토콜이나 커스텀 프로토콜에는 적용 어려움</td>

   </tr>

           <tr>

               <td>터널링, 프로토콜 남용 탐지에 강함</td>
               <td>처리 오버헤드가 클 수 있음</td>

   </tr>

       </tbody>

   </table>

## 5. IDS와 IPS의 차이점

<table>
  <thead>
    <tr>
      <th>IDS</th>
      <th>IPS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <ul>
          <li>탐지 후 경보만 발송</li>
          <li>트래픽 경로 밖(Out-of-band)에 위치</li>
          <li>트래픽 흐름에 영향 없음</li>
          <li>오탐이 발생해도 서비스 중단 없음</li>
          <li>관리자의 수동 대응 필요</li>
          <li>주로 사후 분석, 포렌식에 활용</li>
        </ul>
      </td>
      <td>
        <ul>
          <li>탐지 즉시 자동 차단</li>
          <li>트래픽 경로 내(Inline)에 위치</li>
          <li>트래픽 지연(Latency) 발생 가능</li>
          <li>오탐 시 정상 트래픽도 차단될 위험</li>
          <li>자동화된 실시간 대응</li>
          <li>주로 능동적 방어에 활용</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

<table>

       <thead>

           <tr>
     <th>구분</th>      <th>IDS</th>      <th>IPS</th>
   </tr>

       </thead>

       <tbody>

           <tr>
     <td>주요 기능</td>      <td>탐지 + 경보</td>      <td>탐지 + 차단</td>
   </tr>

           <tr>
     <td>배치 위치</td>      <td>네트워크 경로 외부 (미러링)</td>      <td>네트워크 경로 내부 (인라인)</td>
   </tr>

           <tr>
     <td>대응 방식</td>      <td>수동 (관리자 판단)</td>      <td>자동 (실시간)</td>
   </tr>

           <tr>
     <td>서비스 영향</td>      <td>없음</td>      <td>오탐 시 정상 트래픽 차단 위험</td>
   </tr>

           <tr>
     <td>성능 영향</td>      <td>거의 없음</td>      <td>처리 지연 가능</td>
   </tr>

           <tr>
     <td>주 활용</td>      <td>모니터링, 포렌식, 규정 준수</td>      <td>실시간 방어, 자동화된 대응</td>
   </tr>

       </tbody>

   </table>

실제로 현장에서는 IDS와 IPS를 따로 쓰기보다는 같이 운영하거나, 아예 IDPS(Intrusion Detection and Prevention System)라고 부르는 통합 시스템을 사용하는 경우가 많다. 탐지는 IDS가 하고, 확실한 공격에 대해서는 IPS가 차단하는 식으로 역할을 나누는 것이다.<br>

### 같은 이벤트, 다른 대응 — 탐지 로그 예시

같은 SQL Injection 시도가 발생했을 때 IDS와 IPS가 어떻게 다르게 반응하는지 로그 예시로 보면 차이가 더 직관적으로 보인다.<br>

**IDS — 경보(Alert)만 발생**

```text
[ALERT] SQL Injection Attempt Detected
Timestamp : 2026-05-28 02:14:33
Source IP : 203.0.113.10:54821
Dest IP   : 10.0.0.5:443
Payload   : GET /login?id=' OR '1'='1' -- HTTP/1.1
Rule      : SID:1000021 (SQL Injection - Classic)
Action    : ALERT -> 관리자에게 경보 전송, 트래픽은 통과
```

**IPS — 탐지 즉시 차단(Drop)**

```text
[DROP] SQL Injection Attempt Blocked
Timestamp : 2026-05-28 02:14:33
Source IP : 203.0.113.10:54821
Dest IP   : 10.0.0.5:443
Payload   : GET /login?id=' OR '1'='1' -- HTTP/1.1
Rule      : SID:1000021 (SQL Injection - Classic)
Action    : DROP -> 패킷 차단, 연결 종료
```

발생한 이벤트는 동일하지만, Action 부분에서 차이가 발생한다. IDS는 경보만 남기고 트래픽을 통과시키지만, IPS는 그 자리에서 패킷을 드롭하고 연결을 끊는다.<br>

## 6. IDS/IPS의 장점과 단점

<table>
  <thead>
    <tr>
      <th>장점</th>
      <th>단점</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <ul>
          <li>방화벽이 놓치는 애플리케이션 계층 공격 탐지 가능</li>
          <li>실시간 모니터링으로 빠른 이상 징후 파악</li>
          <li>공격 로그와 증거 데이터 자동 수집 → 포렌식에 유용</li>
          <li>IPS는 자동 차단으로 인력 없이도 즉각 대응 가능</li>
          <li>컴플라이언스 요건 충족에 도움</li>
          <li>내부 네트워크 트래픽 모니터링 가능</li>
        </ul>
      </td>
      <td>
        <ul>
          <li>오탐(False Positive): 정상 트래픽을 공격으로 잘못 판단</li>
          <li>미탐(False Negative): 실제 공격을 놓치는 경우</li>
          <li>암호화된 트래픽(TLS/SSL) 분석 어려움</li>
          <li>고성능 환경에서 처리 속도 병목 발생 가능</li>
          <li>시그니처 DB 지속적 업데이트 필요</li>
          <li>규칙 튜닝에 전문 인력과 시간 필요</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

오탐과 미탐의 트레이드오프가 가장 큰 숙제다. 탐지 기준을 너무 타이트하게 잡으면 정상 서비스가 막히고, 너무 느슨하게 잡으면 공격을 놓친다. 현장에서 IDS/IPS 운영의 상당 부분이 이 밸런스를 맞추는 튜닝 작업이다.<br>

## 7. IDS/IPS의 활용 사례

<table>

       <thead>

           <tr>
     <th>환경</th>      <th>활용 방식</th>      <th>주요 탐지 대상</th>
   </tr>

       </thead>

       <tbody>

           <tr>

               <td>금융기관</td>
               <td>인터넷 뱅킹 서버 앞단에 IPS 배치</td>
               <td>SQL Injection, 계정 탈취 시도, 비정상 거래</td>

   </tr>

           <tr>

               <td>병원 / 의료기관</td>
               <td>EMR 서버 접근 모니터링 (HIDS)</td>
               <td>내부자 무단 접근, 환자 정보 유출 시도</td>

   </tr>

           <tr>

               <td>기업 내부망</td>
               <td>NIDS로 내부 트래픽 전수 분석</td>
               <td>랜섬웨어 확산, 횡적 이동(Lateral Movement)</td>

   </tr>

           <tr>

               <td>클라우드 환경</td>
               <td>WAF + IPS 결합 운영</td>
               <td>웹 애플리케이션 공격, API 남용</td>

   </tr>

           <tr>

               <td>산업제어시스템(ICS)</td>
               <td>OT 네트워크 전용 IDS 운영</td>
               <td>프로토콜 변조, 비인가 제어 명령</td>

   </tr>

           <tr>

               <td>정부기관 / 공공</td>
               <td>보안관제센터 또는 침해대응 체계와 연동</td>
               <td>APT, 스피어 피싱, DDoS</td>

   </tr>

       </tbody>

   </table>

특히 최근에는 클라우드 환경이 많아지면서 전통적인 네트워크 경계가 흐려지고 있다. 이 때문에 네트워크 단의 NIDS/IPS만으로는 부족하고, 각 호스트나 컨테이너 단위의 HIDS, 그리고 클라우드 서비스 제공자(AWS, Azure 등)가 제공하는 보안 서비스와 연동하는 방식으로 진화하고 있다.

## 8. 대표적인 IDS/IPS 도구

| 도구 | 유형 | 설명 |
| --- | --- | --- |
| Snort | NIDS/IPS, 오픈소스 | Cisco가 후원하는 대표적인 오픈소스 IDS/IPS. 시그니처 기반 탐지가 강력하고, 커뮤니티 규칙셋이 방대하다. 모드에 따라 탐지만 하거나 인라인 차단도 가능하다. |
| Suricata | NIDS/IPS, 오픈소스 | OISF가 개발. Snort 규칙 형식과 호환되면서 멀티스레드 처리로 고속 환경에서 성능이 뛰어나다. 네트워크 트래픽 분석(NSM) 기능도 강력하다. |
| Zeek (구 Bro) | NSM / 분석 중심, 오픈소스 | 네트워크 트래픽을 구조화된 로그로 남기고 분석하는 데 강점이 있는 도구다. 포렌식과 위협 헌팅에 자주 쓰이며, SIEM과 연동하는 경우가 많다. |
| OSSEC | HIDS, 오픈소스 | 파일 무결성 검사, 로그 분석, 루트킷 탐지 기능을 제공하는 호스트 기반 IDS다. |
| Wazuh | HIDS / SIEM / XDR, 오픈소스 | OSSEC 기반 확장형 플랫폼. 로그 수집·분석·대응을 하나의 플랫폼에서 처리하고 클라우드 환경 지원이 좋다. |
| Cisco Firepower / Palo Alto | NIDS/IPS, 상용 | 기업 환경에서 많이 쓰이는 상용 NGIPS. DPI, 애플리케이션 식별, 위협 인텔리전스 연동 등 고급 기능을 제공한다. |

## 9. 침해사고 대응 관점에서의 IDS/IPS

IR 관점에서 IDS/IPS는 단순한 탐지 도구 이상의 역할을 한다. 침해사고 대응 사이클에서 각 단계별로 어떻게 쓰이는지 보면 이렇다.<br>

<table>

       <thead>

           <tr>
     <th>IR 단계</th>      <th>IDS/IPS 역할</th>
   </tr>

       </thead>

       <tbody>

           <tr>

               <td><strong>준비 (Preparation)</strong></td>
               <td>탐지 규칙 사전 정의, 기준선(Baseline) 수립, 경보 체계 구성</td>

   </tr>

           <tr>

               <td><strong>탐지 및 분석 (Detection &amp; Analysis)</strong></td>
               <td>실시간 경보 발생 → 이벤트 분류 및 우선순위 결정. IDS 로그가 초기 조사의 핵심 증거가 됨</td>

   </tr>

           <tr>

               <td><strong>봉쇄 (Containment)</strong></td>
               <td>IPS가 공격 IP 자동 차단, 감염 호스트 격리 트리거 가능</td>

   </tr>

           <tr>

               <td><strong>제거 및 복구 (Eradication &amp; Recovery)</strong></td>
               <td>IDS 로그로 공격 경로 추적, 어디까지 침투했는지 타임라인 재구성</td>

   </tr>

           <tr>

               <td><strong>사후 활동 (Post-Incident)</strong></td>
               <td>수집된 로그 분석으로 새 시그니처 추가, 보안 정책 개선</td>

   </tr>

       </tbody>

   </table>

특히 탐지 및 분석 단계에서 IDS 로그가 얼마나 잘 수집되고 있느냐가 IR의 질을 결정한다고 해도 과언이 아니다. IDS가 없거나 로그가 제대로 보존되지 않으면, 침해사고 발생 후 어디서 어떻게 들어왔는가를 밝히는 포렌식 분석 자체가 어려워진다.<br>

IDS/IPS가 아무리 잘 돼 있어도, 경보를 받아서 분석하고 판단하는 사람이 없으면 의미가 없다. 결국 시스템과 사람이 함께 돌아가야 제대로 된 대응이 가능하다는 것이 핵심.<br>

최근에는 IDS/IPS가 단독으로 쓰이기보다는 SIEM(Security Information and Event Management)과 연동해서, 여러 소스의 로그를 한 곳에서 통합 분석하고 대응하는 방식으로 발전하고 있다. SOAR(Security Orchestration, Automation and Response)와 연결하면 IPS의 차단 액션도 자동화 플레이북으로 관리할 수 있다.<br>

## 10. 정리

<table>

       <thead>

           <tr>
     <th>항목</th>      <th>IDS</th>      <th>IPS</th>
   </tr>

       </thead>

       <tbody>

           <tr>
     <td>역할</td>      <td>탐지 + 경보</td>      <td>탐지 + 자동 차단</td>
   </tr>

           <tr>
     <td>위치</td>      <td>Out-of-band (미러링)</td>      <td>Inline (경로 내)</td>
   </tr>

           <tr>
     <td>대응 속도</td>      <td>관리자 개입 필요</td>      <td>실시간 자동 대응</td>
   </tr>

           <tr>
     <td>탐지 방식</td>      <td colspan="2">시그니처 / 이상 행위 / 정책 기반 / 상태 기반 프로토콜 분석 (공통)</td>
   </tr>

           <tr>
     <td>서비스 영향</td>      <td>없음</td>      <td>오탐 시 서비스 중단 위험</td>
   </tr>

           <tr>
     <td>주 강점</td>      <td>로그 보존, 포렌식, 낮은 위험</td>      <td>실시간 방어, 자동화</td>
   </tr>

           <tr>
     <td>대표 도구</td>      <td>Snort(탐지 모드), Suricata(탐지 모드), Zeek, OSSEC/Wazuh</td>      <td>Snort(인라인 모드), Suricata(인라인 모드), 상용 NGIPS</td>
   </tr>

       </tbody>

   </table>

IDS와 IPS는 서로 경쟁하는 기술이 아니라 보완하는 기술이다. 오탐이 걱정되거나 정밀한 분석이 필요한 구간에는 IDS를, 즉각적인 차단이 필요한 구간에는 IPS를 배치하는 방식으로 같이 운영하는 게 일반적이다.<br>

공부하면서 가장 인상 깊었던 건, 결국 IDS/IPS의 효과는 도구 자체의 성능보다 "탐지 규칙을 얼마나 잘 만들고 지속적으로 관리하느냐"에 달려 있다는 점이다. 아무리 좋은 도구를 써도 규칙이 부실하면 구멍 뚫린 방어선이 되고, 반대로 잘 튜닝된 규칙과 꾸준한 로그 모니터링이 있으면 적은 자원으로도 효과적인 방어가 가능하다는 점이 인상 깊었다,<br>

## 참고자료

- [Snort 공식 문서](https://www.snort.org/documents) — Cisco Snort, snort.org
- [Suricata 공식 문서](https://docs.suricata.io) — OISF, docs.suricata.io
- [Zeek 공식 문서](https://docs.zeek.org) — Zeek Project, docs.zeek.org
- [Wazuh 공식 문서](https://documentation.wazuh.com) — Wazuh, documentation.wazuh.com
- [NIST SP 800-94: Guide to Intrusion Detection and Prevention Systems (IDPS)](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-94.pdf) — Karen Scarfone, Peter Mell, NIST, 2007
- [MITRE ATT&CK Framework](https://attack.mitre.org) — 침입 탐지 규칙 설계 참고
