Qualtrics.SurveyEngine.addOnload(function() {

    var num = 32;
    var anum = 24;
    var bnum = 8;
    var aco = 0;
    var bco = 0;

    var strRight = 'T';
    var strLeft = 'W';

    var time = 2000; // 表示時間を2秒に変更
    // 消す問題のQID
    id = "QID152";
    jQuery("#" + id).toggle(false);
    var nextButton = document.getElementById('NextButton');
    nextButton.style.display = 'none';

    // ランダム化関数
    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    // 配列作成関数
    function createElements(atariCount, hazureCount, label) {
        let elements = [];
        for (let i = 0; i < atariCount; i++) {
            elements.push(' アタリ ＋１万円');
        }
        for (let i = 0; i < hazureCount; i++) {
            elements.push('ハズレ ー１万円');
        }
        shuffle(elements);
        return elements;
    }

    // セルのスタイルを決定する関数
    function getCellStyle(content) {
        if (content.includes(' アタリ ＋１万円')) {
            return 'background-color: #FFEBCD;';
        } else if (content.includes('ハズレ ー１万円')) {
            return 'background-color: #E0FFFF;';
        } else {
            return 'background-color: #DCDCDC;'; // アタリでもハズレでもない場合
        }
    }

    // 選択した選択肢名を取得する関数
    function getChoices(trial) {
        if (trial.a == '') {
            return strLeft;
        } else {
            return strRight;
        }
    }

    var aElements = createElements(aco, anum - aco, strRight);
    var bElements = createElements(bco, bnum - bco, strLeft);

    // 32試行の配列を作成
    var trials = new Array(num).fill(null).map(function(_, index) {
        return { trial: index + 1, a: '', b: '' };
    });

    // AとBの要素を試行配列にランダムに配置
    aElements.forEach(function(element) {
        let placed = false;
        while (!placed) {
            let randomIndex = Math.floor(Math.random() * trials.length);
            if (trials[randomIndex].a === '') {
                trials[randomIndex].a = element;
                placed = true;
            }
        }
    });

    bElements.forEach(function(element) {
        let placed = false;
        while (!placed) {
            let randomIndex = Math.floor(Math.random() * trials.length);
            if (trials[randomIndex].b === '' && trials[randomIndex].a === '') {
                trials[randomIndex].b = element;
                placed = true;
            }
        }
    });

    var buttonId = "myButton";
    var buttonClicked = false;

    this.disableNextButton();
    this.hideNextButton();
    var that = this;

    var matrixDisplay = document.getElementById('matrixDisplay');
    matrixDisplay.innerHTML = '<tr><td>順番</td><td>選択</td><td>スロットマシン<b>' + strRight + '</b>の結果</td><td>スロットマシン<b>' + strLeft + '</b>の結果</td></tr>';
    matrixDisplay.innerHTML += '<tr><td >　</td><td>　</td><td >　</td><td>　</td></tr>';

    var currentTrialIndex = 0;
	
	
	function shownull(){
		 var secondRow = matrixDisplay.rows[1];
         secondRow.innerHTML = '<tr><td >　</td><td>　</td><td >　</td><td>　</td></tr>';
	}
	
		function showtextnull(){
					document.getElementById('myDiv').innerText = ' ';
	}
	
    function showNextElement() {
        if (currentTrialIndex < trials.length) {
            var trial = trials[currentTrialIndex];
            var aStyle = getCellStyle(trial.a);
            var bStyle = getCellStyle(trial.b);
            var choices = getChoices(trial);

            var secondRow = matrixDisplay.rows[1];
            secondRow.innerHTML = '<tr><td>' + (currentTrialIndex + 1) + '</td><td>' + choices + '</td><td style="' + aStyle + '">' + trial.a + '</td><td style="' + bStyle + '">' + trial.b + '</td></tr>';

            currentTrialIndex++;
        } else {
            Qualtrics.SurveyEngine.setEmbeddedData('TestTrials', JSON.stringify(trials));
            that.enableNextButton();
            that.showNextButton();
            jQuery("#" + id).toggle(true);
        }
    }
	
	function ChangeButtonName(ct){
		if(ct < 32){
		   document.getElementById('myButton').innerText = '次の履歴を表示するには「Spase」を押してください';
		}if(ct == 32){
			document.getElementById('myButton').innerText = '「Spase」を押して質問に回答してください';
		}
		if(ct>32){
			document.getElementById('myButton').innerText = '次のページに進んでください';
		}
		
	}
	
	function showtext(ct){
		//document.getElementById("myDiv").innerHTML = " 次の履歴を表示するには「Spase」を押してください";
		if(ct < 32){
		   document.getElementById('myDiv').innerText = '次の履歴を表示するには「Spase」を押してください';
		}if(ct == 32){
			document.getElementById('myDiv').innerText = '「Spase」を押して質問に回答してください';
		}
		if(ct>32){
			document.getElementById('myDiv').innerText = '次のページに進んでください';
		}
	}
	
	
			jQuery("#" + buttonId).on("click", function() {
				if (!buttonClicked) {
					buttonClicked = true;

					showNextElement(); // 最初の要素を表示
					
					//ボタン削除
					document.getElementById('myButton').innerText = ' ';
					

					// 2秒ごとにスペースボタンが反応するようにする
					let canPressSpace = false;
					let ct = 1;
					//ChangeButtonName(ct);
					
					setTimeout(function() {
								canPressSpace = true;
								shownull();
								showtext(ct);
						
							}, 2000);

						
					document.addEventListener('keydown', function(event) {
						if (event.code === 'Space' && canPressSpace&&ct<33) {
							showNextElement();
							canPressSpace = false;
							ct++; 
							//ChangeButtonName(ct);
							showtextnull();

							// 2秒後に再びスペースボタンが反応するようにする
							setTimeout(function() {
								canPressSpace = true;
								shownull();
								showtext(ct);
							}, 2000);
						}
					});
				}
			});



});