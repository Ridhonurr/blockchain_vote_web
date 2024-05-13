const eventSource = new EventSource('/transactions');

eventSource.onmessage = function(event) {
    const transactions = JSON.parse(event.data);
    const transactionList = document.getElementById('transaction-list');
    transactionList.innerHTML = '';

    transactions.forEach(transaction => {
        const listItem = document.createElement('li');
        listItem.classList.add('transaction-item');
        listItem.innerHTML = `
            <p><strong>Vote Index:</strong> ${transaction['Vote Index']}</p>
            <p><strong>Timestamp:</strong> ${transaction['Timestamp']}</p>
            <p><strong>Data:</strong> ${transaction['Data']}</p>
            <p><strong>Previous Hash:</strong> ${transaction['Previous Hash']}</p>
            <p><strong>Hash:</strong> ${transaction['Hash']}</p>
        `;
        transactionList.appendChild(listItem);
    });
};
