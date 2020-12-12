def f(s):b=1;exec('print(" "*(s-1)+"*"*b);s-=1;b+=2;'*s)

f(6)

def e(a,b,s):x='print(s*a);';exec(x+'print(s," "*(a-4),s);'*(b-2)+x)

e(6,10,'O')