#debug mode
#CPPFLAGS=-g -Wextra -Wno-sign-compare
LIBS=-lm -lgmp -lgmpxx

# fast mode
CPPFLAGS=-O5

test timeTest: %: %.cpp sparseInt.h
	$(CXX) $(CPPFLAGS) -o $@ $< $(LIBS)
