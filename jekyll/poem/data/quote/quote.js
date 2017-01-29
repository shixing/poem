// When the DOM is ready, run this function
function random_array(start,end){
    l = []
    for (i = start; i < end; i += 1){
	l.push(i);
    }
    for (i = 0; i < end-start; i += 1){
	r = Math.floor(Math.random() * (end-start-i)) + i ;
	temp = l[i];
	l[i] = l[r];
	l[r] = temp;
    }
    return l;
    
}

$(document).ready(function() {
    quotes = ["I like nonsense.  It wakes up the brain cells.","Poets say science takes away from the beauty of the stars ... I too can see the stars on a desert night, and feel them. But do I see less or more?","I read poetry to save time.","A poet can survive everything but a misprint.","I\'m fascinated by rap and by hip-hop.","Why should poetry have to make sense?","I wrote some of the worst poetry west from the Mississippi River, but I wrote. And I finally sometimes got it right.","Poetry is the synthesis of hyacinths and biscuits.","When I was writing pretty poor poetry, this girl with midnight black hair told me to go on.","All bad poetry springs from genuine feeling.","You don\'t make a poem with ideas, but with words.","Poetry is necessary, but is the poet?","It\'s not easy to define poetry.","I\'ve written some poetry I don\'t understand myself.","Listen, real poetry doesn\'t say anything; it just ticks off the possibilities.","I\'ve got poetry in my fingertips ... I\'m an F-18, bro.  And I will destroy you in the air.","Well you can\'t teach the poetry, but you can teach the craft.","You know, bad poetry I wrote in high school can still be found on the Internet.","Sometimes poetry, it is incomprehensible. But we need incomprehensible stuff!","One thing I do know is that poetry, to be understood, must be clear.","Science is for those who learn, poetry is for those who know.","Poetry is the key to the hieroglyphics of nature.","Well, I still write poetry, but I wouldn\'t call myself a poet.","Poetry is not a matter of feelings, it is a matter of language. It is language which creates feelings.","Poetry and lyrics are very similar. Making words bounce off a page.","I was reading the dictionary. I thought it was a poem about everything.","Poetry is what gets lost in translation.","I don\'t think I\'ve ever read poetry, ever.","The poets have been mysteriously silent on the subject of cheese.","In poetry, everything can be faked but the intensity of utterance.","I was a 16-year-old girl at one point, so of course I wrote poetry.","You don\'t have to live in a garage to write great poetry.","Poetry takes courage because you have to face things and you try to articulate how you feel.","Is there any purpose to translating poetry? A poem does not contain information of importance, like a signpost or a warning notice.","The poet doesn\'t invent. He listens.","Unbeing dead isn\'t being alive.","I don\'t care what you say to me. I care what you share with me.","How poetry comes to the poet is a mystery.","Reality leaves a lot to the imagination.","What can be explained is not poetry.","Poetry = Anger x Imagination","This poetry.  I never know what I\'m going to say.","Safety isn\'t always safe.  You can find one on every gun.","Poetry is a way of taking life by the throat.","Love is a clash of lightnings.","Rhythm must have meaning.","He wanted to be a poet ... said he\'d only lacked the words to be one.","A poet who reads his verse in public may have other nasty habits."]
    names = ["Dr. Seuss","Richard Feynman","Marilyn Monroe","Oscar Wilde","John F. Kerry","Charlie Chaplin","Maya Angelou","Carl Sandburg","Carl Sandburg","Oscar Wilde","Stephane Mallarme","Carlos Drummond de Andrade","Bob Dylan","Carl Sandburg","Jim Morrison","Charlie Sheen","David Hockney","Lena Dunham","Roberto Benigni","Mary Oliver","Joseph Roux","David Hare","David Duchovny","Umberto Eco","Taylor Swift","Steven Wright","Robert Frost","Eminem","Gilbert K. Chesterton","Seamus Heaney","Elizabeth Edwards","Felix Dennis","Edward Hirsch","James Buchan","Jean Cocteau","E. E. Cummings","Santosh Kalwar","John Lennon","John Lennon","W. B. Yeats","Sherman Alexie","Jalaluddin Rumi","Andrea Gibson","Robert Frost","Pablo Neruda","Ezra Pound","Nora Roberts","Robert Heinlein"]
    
    quote_html = `
          <div class="item">
            <blockquote>
              <div class="row">
                <div class="col-sm-9">
                  <p>__quote__</p>
                  <small>__name__</small>
                </div>
              </div>
            </blockquote>
          </div>
`;

    quote_html_first = `
          <div class="item active">
            <blockquote>
              <div class="row">
                <div class="col-sm-9">
                  <p>__quote__</p>
                  <small>__name__</small>
                </div>
              </div>
            </blockquote>
          </div>
`;

    html = "";
    l = random_array(0,names.length);

    for (i = 0; i< l.length; i+=1){
	index = l[i];
	quote = quotes[index];
	name = names[index];
	temp_html = '';
	if (i == 0){
	    temp_html = quote_html_first.replace("__quote__",quote).replace("__name__",name);
	} else {
	    temp_html = quote_html.replace("__quote__",quote).replace("__name__",name);
	}
	
	html += temp_html;
    }
    
    $('#quote_inner').html(html);




  //Set the carousel options
  $('#quote-carousel').carousel({
    pause: true,
    interval: 6000,
  });
});
