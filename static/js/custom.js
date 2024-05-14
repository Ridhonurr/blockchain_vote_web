const eventSource = new EventSource('/transactions');

eventSource.onmessage = function(event) {
    const transactions = JSON.parse(event.data);
    const transactionList = document.getElementById('transaction-list');
    transactionList.innerHTML = '';

    transactions.forEach(transaction => {
        const listItem = document.createElement('li');
        listItem.classList.add('transaction-item');
        // Buat teks dengan format yang diinginkan
        const text = `#${transaction['Vote Index']} Timestamp: ${transaction['Timestamp']} Data: ${transaction['Data']} Previous Hash: ${transaction['Previous Hash']} Hash: ${transaction['Hash']}`;
        listItem.textContent = text;
        transactionList.appendChild(listItem);
    });
};

eventSource.onerror = function(event) {
    console.error('Error occurred with SSE connection:', event);
};
