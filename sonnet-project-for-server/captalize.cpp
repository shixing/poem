#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<set>
#include<map>

using namespace std;
ifstream in("data/capitalize_pattern_poem");


map<string,string> word_cap_patt;


void most_probable_pattern(ifstream& in){
	string word,patt;
	while(in>>word>>patt){
		//cout<<word<<endl;
		word_cap_patt[word]=patt;
	}
}

string make_small(string s){
	//string n_word="";
	
	for(int i=0;i<s.length();i++){
		if(s[i]>='A' && s[i]<='Z'){
			s[i]=s[i]-'A'+'a';
		} 
	}
	return s;
}


int main(){
	//cout<<":"<<word_cap_patt["salamu"]<<":"<<endl;
	most_probable_pattern(in);
	
	string line,word;
	while(getline(cin,line)){
	//	cout<<line<<endl;
		stringstream ss(line);
		int count=0;
		while(ss>>word){
				
			count++;
			string print_word;
			if(word_cap_patt[word]==""){
				print_word=word;
			}else{
					print_word=word_cap_patt[word];
			}
			
			if(count==1){
				if(print_word[0]>='a' && print_word[0]<='z')
					print_word[0]=print_word[0]-'a'+'A';
			}
			cout<<print_word<<" ";
			
		}
		cout<<endl;
		
	}
	return 0;
}
