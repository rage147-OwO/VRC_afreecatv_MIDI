const SDK = window.AFREECA.ext;
const extensionSDK = SDK();

// 로그 메시지를 HTML에 추가하는 함수
function addLog(message) {
    const logContainer = document.getElementById("log");
    const logEntry = document.createElement("div");
    logEntry.textContent = message;
    logContainer.appendChild(logEntry);
}

// 초기화 함수
function init() {
    addLog("init() 호출: 초기화가 완료되었습니다.");
}

// AfreecaTV 초기화
extensionSDK.handleInitialization((userInfo, broadInfo, playerInfo) => {
    init();
});

// 로그 정보를 로컬 서버로 전송
function sendLogToServer(message) {
    fetch('http://localhost:49152/log', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ log: message })
    })
    .then(response => {
        if (response.ok) {
            addLog("sendLogToServer() 호출: 로그가 서버에 전송되었습니다.");
        } else {
            addLog("sendLogToServer() 호출: 로그 전송 실패: " + response.status);
        }
    })
    .catch(error => addLog("sendLogToServer() 호출: 서버 전송 중 오류 발생: " + error));
}

// 채팅 정보 수신 처리
const handleChatInfoReceived = (action, message) => {
    addLog("handleChatInfoReceived() 호출: Action received: " + action);
    addLog("handleChatInfoReceived() 호출: Message received: " + JSON.stringify(message));

    switch (action) {
        //case 'MESSAGE':
        //    addLog("handleChatInfoReceived() 호출: Handling MESSAGE action.");
        //    sendLogToServer("handleChatInfoReceived() 호출: MESSAGE action received with: " + JSON.stringify(message));
        //    break;
        case 'BALLOON_GIFTED':
            addLog("handleChatInfoReceived() 호출: Handling BALLOON_GIFTED action.");
            sendLogToServer("handleChatInfoReceived() 호출: BALLOON_GIFTED action received."+JSON.stringify(message));
            break;
        default:
            addLog("handleChatInfoReceived() 호출: Unknown action received: " + action);
    }
}

// 채팅 이벤트 리스너 설정
extensionSDK.chat.listen(handleChatInfoReceived);
