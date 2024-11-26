int soma(int x) {

  if (x < 3) {
    printf(x);
    x = soma(x+1);
  }
  return(x);  
}

void main() {
  int x;
  x = soma(1);
}