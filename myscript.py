from datetime import datetime

f = open(r"/var/www/kofemolka_fa_usr/data/www/kofemolka.fastvps.site/project/demofile3.txt", "a")
time = datetime.now().strftime('%X')
f.write(time + '\n')
f.close()
print('Successfully closed poll')
