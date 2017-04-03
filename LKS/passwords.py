Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:01:18) [MSC v.1900 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> import postgresql
>>> import hashlib
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('123456', 'sudya2', hashlib.md5('1'.encode('utf8')).hexdigest(), 0, 'Dima')

        
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('123457', 'sudya3', hashlib.md5('1'.encode('utf8')).hexdigest(), 0, 'therd')

        
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('123458', 'sudya4', hashlib.md5('1'.encode('utf8')).hexdigest(), 0, 'fourth')

        
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('123459', 'sudya5', hashlib.md5('1'.encode('utf8')).hexdigest(), 0, 'fifth')

        
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('123460', 'sudya6', hashlib.md5('1'.encode('utf8')).hexdigest(), 0, 'sixth')

        
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('sachiv', 'sachivko',  hashlib.md5('sachivkolks'.encode('utf8')).hexdigest(), 0, 'Sachivko')

        
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('titare', 'titarenko',  hashlib.md5('titarenkolks'.encode('utf8')).hexdigest(), 0, 'Titarenko')

        
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('bella0', 'bella',  hashlib.md5('bellalks'.encode('utf8')).hexdigest(), 0, 'Bella')

        
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('vinoku', 'vinokurova',  hashlib.md5('vinokurovalks'.encode('utf8')).hexdigest(), 0, 'Vinokurova')

        
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('maximu', 'maximus',  hashlib.md5('maximuslks'.encode('utf8')).hexdigest(), 0, 'Maximus')

        
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('kenzo0', 'kenzo',  hashlib.md5('kenzolks'.encode('utf8')).hexdigest(), 0, 'Kenzo')

        
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('zulu0', 'zulu',  hashlib.md5('zululks'.encode('utf8')).hexdigest(), 0, 'Zulu')

        
>>> with postgresql.open('pq://postgres:poqwiueryt@localhost/LKS') as db:
        sel = db.prepare("INSERT INTO log_pass values($1, $2, $3, $4, $5)")
        jud = sel('hmel', 'hmel',  hashlib.md5('hmellks'.encode('utf8')).hexdigest(), 0, 'Hmel')
