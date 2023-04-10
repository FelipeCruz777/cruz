import matplotlib.pyplot as plt
from sys import getsizeof
import time
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="myusername",
    password="mypassword",
    database="mydatabase"
)
mycursor = mydb.cursor()

sizes = range(20, 31)
l1 = []

for n in sizes:
    data = 'transaction01' * n
    print(data)
    b = data.encode()
    start = time.time()
    max_mem = 0
    min_mem = 0
    while b:
        if n == len(b):
            max_mem = getsizeof(b) - getsizeof(b'')
        elif len(b) == 1:
            min_mem = getsizeof(b) - getsizeof(b'')
        b = b[1:]
    stop = time.time()
    print(f'Valor {n} {stop-start} - Max mem {max_mem/10**3} KB - Min mem {min_mem} B')
    l1.append(stop - start)

l2 = []
for n in sizes:
    data = b'x' * n
    b = memoryview(data)
    start = time.time()
    max_mem = 0
    min_mem = 0
    while b:
        if n == len(b):
            max_mem = getsizeof(b) - getsizeof(b'')
        elif len(b) == 1:
            min_mem = getsizeof(b) - getsizeof(b'')
        b = b[1:]
    stop = time.time()
    sql = "INSERT INTO temperatura (temperatura) VALUES (%s)"
    val = (n,)
    mycursor.execute(sql, val)
    mydb.commit()
    print(f'Temperatura {n} {stop-start} - Max mem {max_mem/10**3} KB - Min mem {min_mem} B')
    l2.append(stop - start)

plt.plot(l1,'x--', label="Without Memoryview")
plt.plot(l2,'o--', label="With Memoryview")
plt.xlabel('Size of Bytearray')
plt.ylabel('Time (S)')
plt.legend()
plt.show()
