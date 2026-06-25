# ConnecT 🌐

> **Application to Infrastructure, Connected Simply.**
> 웹 프레임워크 소스 코드와 복잡한 클라우드 인프라 구성을 직관적으로 연결하는 선언형 배포 전용 DSL (Domain-Specific Language).

ConnecT는 개발자가 Nginx 설정, Docker Compose 파일 작성, SSL 인증서 발급, 네트워크 포트 포워딩 인프라를 일일이 수동으로 제어하며 겪는 피로를 해결하기 위해 설계되었습니다. 실제 서비스 로직은 익숙한 프레임워크(Flask, FastAPI, Node.js 등)로 작성하고, 배포 아키텍처 기술은 ConnecT의 직관적인 `.ct` 파일 단 몇 줄로 추상화하세요.

---

## 🚀 Key Features

* **최상의 개발자 경험 (DX):** 재귀 하강 파서(Recursive Descent Parser) 기반 설계로 문법 에러 발생 시 정확한 키워드 라인 넘버를 추적하여 디버깅이 명확합니다.
* **엄격한 정적 검증 (Strict Validation):** 컴파일 단계에서 중복 속성 선언, 유효 범위를 벗어난 포트(1-65535), 등록되지 않은 엔진을 완벽하게 검단하여 배포 시점의 런타임 에러를 방지합니다.
* **유연한 런타임 & NoSQL 확장:** Flask, FastAPI, Django, Node.js 백엔드는 물론 관계형 DB(MySQL, PostgreSQL)부터 인메모리 및 도큐먼트 NoSQL(Redis, MongoDB)까지 폭넓게 지원합니다.
* **스마트 인프라 컴파일:** 작성된 코드는 유효성 검증을 거쳐 표준화된 JSON 스펙 및 배포 자동화를 위한 실제 인프라 설정 파일로 컴파일됩니다.

---

## 🛠️ 문법 예시 (`production.ct`)

```text
app "web_main" {
    runtime flask
    entrypoint "app.py"
    network {
        domain "example.com"
        port auto
        ssl auto
    }
    env {
        DB_HOST "main_db"
        SECRET_KEY "secret-token-key"
    }
}

database "main_db" {
    engine mysql
    env {
        USER "root"
        PASSWORD "password"
        DATABASE "appdb"
    }
}
