# blockchain_vote_web
Web Application for Implementation Blockchain on Voting System

Saya mengimplementasikan teknologi blockchain pada sistem voting yang saya rancang sendiri.
pada program ini, user yang digunakan untuk database harus dibatasi. tidak memperbolehkan update pada data sehingga akan mengurangi kesempatan seseorang untuk memanipulasinya.

Blockchain Voting System, begitulah saya menyebutnya. setiap data akan terhubung satu sama lain dengan hash, sistem akan mengecek data terakhir sebelum menambahkan data. jika ditemukan sebuah data yang hashnya tidak cocok maka data tersebut akan dihapus dan digantikan oleh data yang baru. sehingga rantai hashnya akan tetap terjaga.

program ini sangat powerfull jika digunakan dalam skala besar seperti pemilihan umum, tetapi harus dilakukan beberapa pembenahan seperti database dari pemilih dan kandidat yang akan dipilih.

saya menggunakan dasar pemahaman dari sistem blockchain yang sangat kompleks, seharusnya untuk memastikan semuanya benar-benar terdesentralisasi dibutuhkan sebuah jaringan validator( jika pada bitcoin disebut penambang/miner ) yang akan terus mengecek valid atau tidaknya sebuah data. namun, saya buat sesimpel mungkin dengan alih-alih menjadi sebuah penambang/miner saya menggantinya menjadi "voter validator".
