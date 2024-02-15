const list = document.createElement('ul');
const info = document.createElement('p');
const html = document.querySelector('html');

info.textContent = 'Below is a dynamic list. Click anywhere on the page to add a new list item. Click an existing list item to change its text to something else.';

document.body.appendChild(info);
document.body.appendChild(list);

html.onclick = function() {
  const listItem = document.createElement('li');
  const listContent = prompt('What content do you want the list item to have?');
  listItem.textContent = listContent;
  list.appendChild(listItem);

  listItem.onclick = function(e) {
    e.stopPropagation();
    const listContent = prompt('Enter new content for your list item');
    this.textContent = listContent;
  }
}



const table_area = document.getElementById("table_area");

generateTable(table_area, array1,array2);

function generateTable(_target, _data, _num, _columns = 10) {
  const _table = document.createElement("table");
  const _tbody = document.createElement("tbody");
  let _counter = 0;
  for (i = 0; i < Math.ceil(_data.length / _columns); i++) {
    const _table_row = document.createElement("tr");
    const _table_row_num = document.createElement("tr");

    for (let j = 0; j < _columns; j++) {
      const _cell = document.createElement("td");
      const _cell_num = document.createElement("td");
      if (_data[_counter]) _cell.innerHTML = _data[_counter];
      if (_num[_counter]) _cell_num.innerHTML = _num[_counter];
      _counter++;
      _table_row.appendChild(_cell);
      _table_row_num.appendChild(_cell_num);
    }
    _tbody.appendChild(_table_row);
    _tbody.appendChild(_table_row_num);

  }
  _table.appendChild(_tbody);
  _target.appendChild(_table);
}




<p>どちらのスロットが良いかを選択してください</p><br>
<div class="field">
<strong></strong></div><div class="field">
<strong>スロット A:</strong>
<strong>スロット B:</strong>
</div>
<div class="field">
<div id="table_area2">&nbsp;</div>
<div id="table_area1">&nbsp;</div>
</div>



.container {
    position: relative;
}
.text-above {
   position: absolute;
   top: -10px;
   left: 20%;
}

<p>どちらのスロットが良いかを選択してください</p><br>
<div class="field">
 <div class="container">
  <div id="table_area1">&nbsp;</div>
  <div class="text-above"><strong>スロット A:</strong></div>
 </div>

 <div class="container">
  <div id="table_area2">&nbsp;</div>
  <div class="text-above"><strong>スロット B:</strong></div>
 </div>

</div>