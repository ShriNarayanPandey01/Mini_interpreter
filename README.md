# Mini_interpreter
this is a mini interpreter that i have implemented via python 
In this mini interpreter we can perform bsaic airthmatic and logical operation on String , int , boolean 

i have also applied the concept of variable scope 

* in my mini interpreter you can assign variable using var key word
* you can print statement using print key word example :  ' print "hello";"
* each line of code should end with semi colon

i have not ye implemented loop , if else and other basic feature but i will add them sure 

working of my mini interpreter 
  step  1 : tokenizer
          check working of tokenizer by using this command in terminal
            ' python main.py tokenize <address of txt file > '
  step  2 : parsing
          check working of pareser by using this command in terminal
            ' python main.py parse <address of txt file > '
  step  3 : evaluating
          check working of evaluating by using this command in terminal
            ' python main.py evaluate <address of txt file > '
  step  4 : final execution
          check working of run by using this command in terminal
            ' python main.py in <address of txt file > '

in order to chk use my interpreter you have to write code in txt file and then in python enviornment 
use command ' python main.py run <address of txt file > '

example of my code that would run 
"""""
{
var a = 5;
var b = "hello";
var c = 6;
var d = c*a;
{
  var b = "my my";
  var e = d*2
  print e;
  print b;
}
print b;
}

""""""

