const eventSource = new EventSource('/transactions');

eventSource.onmessage = function(event) {
    const transactions = JSON.parse(event.data);
    const transactionList = document.getElementById('transaction-list');
    transactionList.innerHTML = '';

    transactions.forEach(transaction => {
        const listItem = document.createElement('li');
        listItem.classList.add('transaction-item');
        
        // Buat teks dengan elemen span untuk memberikan warna
        const text = `
            <span class="vote-index">#${transaction['Vote Index']}</span>
            <span class="timestamp">Timestamp: ${transaction['Timestamp']}</span>
            <span class="data">Data: ${transaction['Data']}</span>
            <span class="previous-hash">Previous Hash: ${transaction['Previous Hash']}</span>
            <span class="hash">Hash: ${transaction['Hash']}</span>
        `;
        listItem.innerHTML = text;
        transactionList.appendChild(listItem);
    });
};

eventSource.onerror = function(event) {
    console.error('Error occurred with SSE connection:', event);
};
