const tg=window.Telegram?.WebApp;if(tg){tg.ready();tg.expand()}const API="";let currentUser=null,currentInvoice=null,currentPlay=null,revealed=false,scratchCtx=null,scratchCanvas=null,isDrawing=false;function fakeUser(){return{id:123456789,username:"demo_user",first_name:"Demo"}}function getTelegramUser(){return tg?.initDataUnsafe?.user||fakeUser()}function showToast(msg){const el=document.getElementById("toast");el.textContent=msg;el.classList.add("show");setTimeout(()=>el.classList.remove("show"),2400)}function money(v){return`R$ ${Number(v||0).toFixed(2)}`}async function api(path,options={}){const res=await fetch(API+path,{headers:{"Content-Type":"application/json"},...options});if(!res.ok){let msg="Erro inesperado";try{const data=await res.json();msg=data.detail||msg}catch(e){}throw new Error(msg)}return res.json()}function screen(id){document.querySelectorAll(".screen").forEach(s=>s.classList.remove("active"));document.getElementById(id).classList.add("active")}async function boot(){try{const tgUser=getTelegramUser();currentUser=await api("/api/telegram/user",{method:"POST",body:JSON.stringify({telegram_id:tgUser.id,username:tgUser.username||null,first_name:tgUser.first_name||"Jogador"})});document.getElementById("userName").textContent=`${currentUser.first_name||"Jogador"} ${currentUser.username?"(@"+currentUser.username+")":""}`;await loadCards()}catch(e){showToast(e.message)}}const RANDOM_COVER_THEMES = [
    { emoji: "💎", cls: "theme-diamond" },
    { emoji: "🔥", cls: "theme-fire" },
    { emoji: "🍀", cls: "theme-luck" },
    { emoji: "👑", cls: "theme-king" },
    { emoji: "🪙", cls: "theme-coin" },
    { emoji: "⭐", cls: "theme-star" },
    { emoji: "🎰", cls: "theme-casino" },
    { emoji: "🌈", cls: "theme-rainbow" }
];

function randomCoverTheme(cardId) {
    const id = Number(cardId || 0);
    return RANDOM_COVER_THEMES[Math.abs(id) % RANDOM_COVER_THEMES.length];
}

function coverHtml(card) {
    if (card.cover_image) {
        return `<div class="card-cover uploaded-cover" style="background-image:url('${card.cover_image}')"></div>`;
    }

    const theme = randomCoverTheme(card.id);
    return `
        <div class="card-cover auto-cover ${theme.cls}">
            <div class="auto-cover-glow"></div>
            <div class="auto-cover-emoji">${theme.emoji}</div>
            <div class="auto-cover-label">Tema automático</div>
        </div>
    `;
}

async function loadCards() {
    const cards = await api("/api/scratch-cards");
    const list = document.getElementById("cardsList");
    list.innerHTML = "";

    cards.forEach(card => {
        const el = document.createElement("div");
        el.className = "scratch-card";

        el.innerHTML = `
            ${coverHtml(card)}
            <div class="scratch-card-body">
                <h3>${card.name}</h3>
                <p>${card.description || "Raspadinha demo"}</p>
                <p class="rule-line">${card.rule_label || ((card.match_count || 3) + " iguais ganha")}</p>
                <div class="stats-line">
                    <span>RTP ${Number(card.rtp || 0).toFixed(2)}%</span>
                    <span>Margem ${Number(card.house_edge || 0).toFixed(2)}%</span>
                </div>
                <div class="price-line">
                    <div>
                        <div class="muted">Valor</div>
                        <div class="price">${money(card.price)}</div>
                    </div>
                    <button class="primary">Jogar</button>
                </div>
            </div>
        `;
        el.querySelector("button").onclick = () => createInvoice(card.id);
        list.appendChild(el);
    });
}async function createInvoice(cardId){try{const invoice=await api("/api/invoice/create",{method:"POST",body:JSON.stringify({telegram_id:currentUser.telegram_id,scratch_card_id:cardId})});currentInvoice=invoice;document.getElementById("invoiceCardName").textContent=invoice.scratch_card;document.getElementById("invoiceAmount").textContent=money(invoice.amount);document.getElementById("invoiceStatus").textContent=invoice.status;document.getElementById("pixCode").value=invoice.pix_code;screen("invoiceScreen")}catch(e){showToast(e.message)}}async function simulatePayment(){try{const invoice=await api("/api/invoice/pay-demo",{method:"POST",body:JSON.stringify({telegram_id:currentUser.telegram_id,invoice_id:currentInvoice.id})});currentInvoice={...currentInvoice,...invoice};document.getElementById("pixKey1").value="";document.getElementById("pixKey2").value="";document.getElementById("pixError").textContent="";screen("pixScreen");showToast("Pagamento demo confirmado.")}catch(e){showToast(e.message)}}async function cancelInvoice(){try{await api("/api/invoice/cancel",{method:"POST",body:JSON.stringify({telegram_id:currentUser.telegram_id,invoice_id:currentInvoice.id})});currentInvoice=null;showToast("Invoice cancelada.");goHome()}catch(e){showToast(e.message)}}async function confirmPix(){const p1=document.getElementById("pixKey1").value.trim(),p2=document.getElementById("pixKey2").value.trim(),err=document.getElementById("pixError");err.textContent="";if(p1.length<3){err.textContent="Chave Pix curta demais.";return}if(p1!==p2){err.textContent="As chaves Pix não batem.";return}try{const invoice=await api("/api/invoice/confirm-pix",{method:"POST",body:JSON.stringify({telegram_id:currentUser.telegram_id,invoice_id:currentInvoice.id,pix_key:p1})});currentInvoice={...currentInvoice,...invoice};await playAndPrepareScratch()}catch(e){showToast(e.message)}}async function playAndPrepareScratch(){try{const play=await api("/api/play-paid",{method:"POST",body:JSON.stringify({telegram_id:currentUser.telegram_id,invoice_id:currentInvoice.id})});currentPlay=play;revealed=false;document.getElementById("scratchTitle").textContent=play.card;buildSymbols(play.symbols||[]);screen("scratchScreen");setTimeout(setupScratchCanvas,120)}catch(e){showToast(e.message)}}function buildSymbols(symbols){const grid=document.getElementById("symbolsGrid");grid.innerHTML="";symbols.forEach(s=>{const cell=document.createElement("div");cell.className="symbol-cell";cell.textContent=s;grid.appendChild(cell)})}function setupScratchCanvas(){scratchCanvas=document.getElementById("scratchCanvas");scratchCtx=scratchCanvas.getContext("2d",{willReadFrequently:true});scratchCtx.globalCompositeOperation="source-over";const grad=scratchCtx.createLinearGradient(0,0,330,330);grad.addColorStop(0,"#cfd6e4");grad.addColorStop(.5,"#aeb7c8");grad.addColorStop(1,"#e5e9f1");scratchCtx.fillStyle=grad;scratchCtx.fillRect(0,0,scratchCanvas.width,scratchCanvas.height);scratchCtx.fillStyle="rgba(255,255,255,.55)";scratchCtx.font="900 26px system-ui";scratchCtx.textAlign="center";scratchCtx.fillText("RASPE AQUI",165,160);scratchCtx.font="700 16px system-ui";scratchCtx.fillText("3 símbolos iguais ganha",165,190);scratchCanvas.onpointerdown=startScratch;scratchCanvas.onpointermove=scratchMove;scratchCanvas.onpointerup=stopScratch;scratchCanvas.onpointerleave=stopScratch}function pointerPos(evt){const rect=scratchCanvas.getBoundingClientRect();return{x:(evt.clientX-rect.left)*(scratchCanvas.width/rect.width),y:(evt.clientY-rect.top)*(scratchCanvas.height/rect.height)}}function startScratch(evt){isDrawing=true;scratchAt(evt)}function scratchMove(evt){if(!isDrawing)return;scratchAt(evt)}function stopScratch(){isDrawing=false;checkReveal()}function scratchAt(evt){evt.preventDefault();const p=pointerPos(evt);scratchCtx.globalCompositeOperation="destination-out";scratchCtx.beginPath();scratchCtx.arc(p.x,p.y,24,0,Math.PI*2);scratchCtx.fill();if(Math.random()>.86)checkReveal()}function revealPercent(){const img=scratchCtx.getImageData(0,0,scratchCanvas.width,scratchCanvas.height),pixels=img.data;let transparent=0;for(let i=3;i<pixels.length;i+=4){if(pixels[i]<80)transparent++}return transparent/(pixels.length/4)}function checkReveal(){if(revealed)return;if(revealPercent()>.48){revealed=true;scratchCtx.clearRect(0,0,scratchCanvas.width,scratchCanvas.height);setTimeout(showResult,700)}}function autoScratch(){if(!scratchCtx||revealed)return;let steps=0;const timer=setInterval(()=>{scratchCtx.globalCompositeOperation="destination-out";for(let i=0;i<8;i++){const x=Math.random()*scratchCanvas.width,y=Math.random()*scratchCanvas.height;scratchCtx.beginPath();scratchCtx.arc(x,y,28,0,Math.PI*2);scratchCtx.fill()}steps++;if(steps>18){clearInterval(timer);revealed=true;scratchCtx.clearRect(0,0,scratchCanvas.width,scratchCanvas.height);setTimeout(showResult,500)}},55)}function showResult(){const play=currentPlay;document.getElementById("resultIcon").textContent=play.won?"🎉":"😬";document.getElementById("resultTitle").textContent=play.won?"Você ganhou!":"Não foi dessa vez";document.getElementById("resultText").textContent=play.won?"Payout demo enviado automaticamente para a chave Pix confirmada.":"A invoice foi usada e a jogada ficou registrada no admin.";document.getElementById("resultPrize").textContent=money(play.prize);document.getElementById("resultPix").textContent=play.player_pix_key||"-";document.getElementById("resultPayout").textContent=play.payout_status||"-";document.getElementById("resultHash").textContent=play.result_hash||"-";screen("resultScreen");if(tg?.HapticFeedback){play.won?tg.HapticFeedback.notificationOccurred("success"):tg.HapticFeedback.notificationOccurred("warning")}}function goHome(){currentInvoice=null;currentPlay=null;screen("cardsScreen");loadCards()}boot();
