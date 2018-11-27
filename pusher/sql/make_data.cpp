#include <fstream>
#include <cstdlib>
#include <ctime>
#include <array>
#include <string>
#include <iostream>
using std::array; using std::srand;
using std::rand; using std::time; 
using std::ofstream; using std::string;
using std::cout; using std::endl;
using std::to_string;

void make_messages (ofstream&,int);

int main () {
	srand(time(nullptr));

	ofstream out("data.sql");
	for (int i = 0; i < 4; ++i) {
		make_messages(out,i);
		out << endl;
	}

return 0;
}

void make_messages (ofstream& out, int room) {
  array <string,9> users { "User1","User2","User3","User4","User5",
                           "User6","User7","User8","User9" };
  array <string,4> rooms { "Global","Test_Room_1","Test_Room_2","Test_Room_3"};
  array <string,15> messages { "One","Two","Three","Four","Five",
                              "This","Is","A","Test","To","Test","Test","Room","Number",to_string(room) };

  out << "INSERT INTO messages VALUES" << endl;
  for (int i = 0; i < 15; ++i) {
  	out << "(default,'" + users[rand()%6] + "','" + rooms[room] + "','" + 
           messages[i] + "','2018-11-" + to_string(i+1) + " 12:34:56')";
  	if (i<14) {
  		out << "," << endl;
  	}
  }
  out << ";";
}