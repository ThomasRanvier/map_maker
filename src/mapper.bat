
javac -cp .;../lib/* -sourcepath . Main.java -d ../out/

cd ../out

java -cp .;../lib/* Main "http://localhost" 50000 -200 -200 200 200
pause;
