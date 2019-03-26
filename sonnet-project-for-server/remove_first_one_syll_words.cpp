#include<iostream>
#include<fstream>
#include<sstream>
#include<string>


using namespace std;

string remove_first_word(string s){
	size_t found = s.find(" ");
	return s.substr(found+1,s.length());
}

string right_trim(string s){
	int i;
	for(i=s.length()-1;i>=0;i--)
		if(s[i]!=' ')
			break;
	return s.substr(0,i+1);		
}

int main(){
	string s;
	int counter=0;
	bool lastend=true;
	while(getline(cin,s)){
			counter++;
			stringstream ss(s);
			string out=s;
			string w;
			ss>>w;
			if(lastend && (w=="of" || w=="Of"))
				out=remove_first_word(s);
			
			else if(counter==14 && (w=="And" || w=="and" || w=="or" || w=="Or"))
					out=remove_first_word(s);
			string s_c=right_trim(s);
			if(s_c[s_c.length()-1]==',' ||s_c[s_c.length()-1]=='.')
				lastend=true;
			else
				lastend=false;
				
		cout<<out<<endl;
	}
	
	//cout<<":"<<remove_first_word("of my girl.")<<":"<<endl;
	//cout<<right_trim("hi")<<":"<<endl;
	return 0;
}
