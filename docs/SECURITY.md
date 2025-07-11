# 보안 가이드

## 인증 설정

Browser Use WebUI는 기본적으로 로그인 인증이 활성화되어 있습니다.

### 기본 설정

기본 관리자 계정:
- 사용자명: `admin`
- 비밀번호: `browser-use-2024`

⚠️ **중요**: 프로덕션 환경에서는 반드시 기본 비밀번호를 변경하세요!

### 환경변수 설정

`.env` 파일에서 다음 설정을 변경할 수 있습니다:

```env
# 기본 관리자 계정
DEFAULT_USERNAME=your_admin_username
DEFAULT_PASSWORD=your_secure_password

# 여러 사용자 계정 (선택사항)
AUTH_USERS=admin:secure_password,user1:password1,user2:password2

# 비밀번호 해시화 솔트 (보안을 위해 변경 권장)
PASSWORD_SALT=your_unique_salt_string

# 인증 비활성화 (개발 환경에서만 사용)
DISABLE_AUTH=false
```

### 사용자 관리

#### 단일 관리자 계정
```env
DEFAULT_USERNAME=admin
DEFAULT_PASSWORD=my_secure_password_123
```

#### 여러 사용자 계정
```env
AUTH_USERS=admin:admin_password,researcher:research_pass,analyst:analyst_pass
```

### 로그아웃 기능

웹 UI 우상단에 로그아웃 버튼이 제공됩니다:
- 🚪 로그아웃 버튼 클릭 시 세션 종료
- 자동으로 로그인 화면으로 리다이렉트
- 브라우저 새로고침으로 세션 초기화

### 보안 권장사항

1. **강력한 비밀번호 사용**
   - 최소 12자 이상
   - 대소문자, 숫자, 특수문자 조합

2. **솔트 값 변경**
   - `PASSWORD_SALT` 값을 고유한 문자열로 변경

3. **HTTPS 사용**
   - 프로덕션 환경에서는 리버스 프록시(nginx, apache)를 통해 HTTPS 설정

4. **방화벽 설정**
   - 필요한 IP 주소에서만 접근 허용

5. **정기적인 비밀번호 변경**
   - 주기적으로 비밀번호 업데이트

6. **세션 관리**
   - 작업 완료 후 로그아웃 습관화
   - 공용 컴퓨터에서는 반드시 로그아웃
   - 브라우저 종료 시에도 세션 유지되므로 주의
### 인증 비활성화 (권장하지 않음)

개발 환경에서만 인증을 비활성화할 수 있습니다:

```bash
# 명령행 옵션
python webui.py --no-auth

# 환경변수
DISABLE_AUTH=true
```

⚠️ **경고**: 프로덕션 환경에서는 절대 인증을 비활성화하지 마세요!

## Docker 환경에서의 보안

Docker Compose를 사용할 때:

1. `.env` 파일 권한 설정:
   ```bash
   chmod 600 .env
   ```

2. 컨테이너 네트워크 격리
3. 불필요한 포트 노출 방지

## 문제 해결

### 로그인할 수 없는 경우

1. 환경변수 확인:
   ```bash
   echo $DEFAULT_USERNAME
   echo $DEFAULT_PASSWORD
   ```

2. 로그 확인:
   ```bash
   docker-compose logs webui
   ```

3. 인증 비활성화 후 재설정:
   ```bash
   python webui.py --no-auth
   ```

### 비밀번호 재설정

환경변수를 변경한 후 서비스를 재시작하세요:

```bash
# Docker 환경
docker-compose restart

# 로컬 환경
# webui.py 프로세스 종료 후 재시작
```