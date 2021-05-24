
var templateAnswerPanel = document.getElementById('templateAnswerPanel');
var panelCounter = 0;

function loadMessage(panelID, Question, Asker, postDate, Reply, Likes, ImageLink) {   
	//Clone Template Panel
	var clone = templateAnswerPanel.cloneNode(true); // "deep" clone
    clone.id = "panel" + panelID; // there can only be one element with an ID

    //Set Panel to visible
    clone.style = ""

    //Load Panel DataQuestion;
    clone.getElementsByClassName('question')[0].innerText = Question;

    if (Asker.id) {
    	clone.getElementsByClassName('author')[0].innerText = Asker.username;
    	clone.getElementsByClassName('author')[0].style	= "font-weight: 500";
    } else {
    	clone.getElementsByClassName('author')[0].innerText = "Anonymous";
    }
    
    clone.getElementsByClassName('postDate')[0].innerText = postDate;
    clone.getElementsByClassName('reply')[0].innerText = Reply;
    clone.getElementsByClassName('likeCount')[0].innerText = Likes;

    if (ImageLink) {
	    var imageWidth = Math.min(ImageLink.w, 870);
		var imageHeight = (ImageLink.h/ImageLink.w) * imageWidth;
		clone.getElementsByClassName('replyImage')[0].style = "background-image:url(" + ImageLink.img + ");height:"+imageHeight+"px;width:"+ imageWidth + "px;";
    }
    
    //Create new panel
    templateAnswerPanel.parentNode.appendChild(clone);
}

function loadUserData(Username, Followers, Answers, Following, Banner, ProfilePicture) {
	var userInfo = document.getElementById('userInfo');

	document.getElementById('username').innerText = Username;
	document.getElementById('userBannerImage').style = "background-image: url(" + Banner + ")";
	document.getElementById('followers').innerText = Followers;
	document.getElementById('answers').innerText = Answers;
	document.getElementById('following').innerText = Following;
	document.getElementById('profilePicture').style = "background-image: url(" + ProfilePicture + ")";


	document.getElementsByClassName('postProfilePicture').style = "background-image: url(" + ProfilePicture + ")";
	document.getElementsByClassName('postUsername').innerText = Username;

	userInfo.style = "";
	document.getElementById('unloaded').style = "display: none;"
}

const fileSelector = document.getElementById('fileSelector');
  fileSelector.addEventListener('change', (event) => {
    var reader = new FileReader();
    
    reader.onload = function(event) {
	    jsonObj = JSON.parse(event.target.result);
	    jsonLoader(jsonObj);
	  }

    reader.readAsText(event.target.files[0]);
 });


function jsonLoader(json) {
	loadUserData(json.username, json.followers, json.answers, json.following, json.banner, json.avatar)

	jsonObj.posts.forEach( function(entry) {
		try {
			post = entry.post;
			date = new Date(post.timestamp * 1000);
			humanDate = date.getDate() + " " + date.toLocaleString('default', { month: 'short' });

			loadMessage(++panelCounter, post.comment, post.senderData, humanDate, post.reply, post.likes, post.media);
		} catch(err) {
			console.log("Error on: " + panelCounter + " [" + json.id + "]")
			console.log(err)
		}
	});

	console.log(panelCounter)
}