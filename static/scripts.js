// Create a new directed graph
var g = new dagreD3.graphlib.Graph().setGraph({});

var activities = []
var factJsonArray;
var activities;
// var rulesGeneral = ["kettle(A) &rArr; act(A) &and; not duration_gt(A, 130) &and; before_hour(A, 22)",
//     			    "kettle(A) &rArr; act(A) &and; not duration_gt(A, 20) &and; duration_gt(A, 0)",
//     			    "kettle(A) &rArr; act(A) &and; start_hour(A, 11) &and; weekday(A, 4)"];

var rulesGeneral = [    "kettle(A) &rArr; act(A) &and; not duration_gt(A,240) &and; before_hour(A,11) &and; not weekday(A,4), not weekday(A,5) &and; not weekday(A,6)",
    					"kettle(A) &rArr; act(A) &and; not duration_gt(A,240) &and; before_hour(A,12) &and; not before_hour(A,10) &and; weekday(A,4)",
    					"kettle(A) &rArr; act(A) &and; not duration_gt(A,240) &and; not before_hour(A,21) &and; weekday(A,5) &and; weekday(A,6)"];



var rulesDiv = d3.select("#rulesDiv")

rulesGeneral.forEach(function (rule){
	rulesDiv.append('span').html(rule).append('br');
})
rulesDiv.append('br');
rulesDiv.append('br');


fetch('static/DBTest/facts.json').then(response => response.json())
	.then(data => makeList(data)).then(getJSON());

async function getJSON(activity_id = -1){
	//fetch('127.0.0.1:5000/getFacts')

	fetch("/getFacts?"+ new URLSearchParams({
			activity_id: activity_id
		}))
		.then(response => response.json())
	    .then(data => buildGUI(activities, data))
}








//kettle(A) &rArr; duration_gt(A, 50) &and; start_before(A, 11) &and; day(A, 6)

function buildGUI(activities, facts){

	g = new dagreD3.graphlib.Graph().setGraph({});
	var selectedActivity = 'A'

	var activityRadios = document.getElementsByName('activity');
	for(var i = 0; i < activityRadios.length; i++){
		if(activityRadios[i].checked){
			selectedActivity = activityRadios[i].value;
			break;
		}
	}
    selectedActivity = selectedActivity.split("(")[1].split(")")
	var selectedActivityID = selectedActivity[0]

	var variable = selectedActivityID;

	// var rules = ["kettle(${variable}) :- act(${variable}), not duration_gt(${variable},130), before_hour(${variable},22)",
    // 			 "kettle(${variable}) :- act(${variable}), not duration_gt(${variable},20), duration_gt(${variable},0)",
    // 			 "kettle(${variable}) :- act(${variable}), start_hour(${variable},11), weekday(${variable},4)"];

	var rules = ["kettle(${variable}) :- act(${variable}), not duration_gt(${variable},240), before_hour(${variable},11), not weekday(${variable},4), not weekday(${variable},5), not weekday(${variable},6)",
				 "kettle(${variable}) :- act(${variable}), not duration_gt(${variable},240), before_hour(${variable},12), not before_hour(${variable},10), weekday(${variable},4)",
				 "kettle(${variable}) :- act(${variable}), not duration_gt(${variable},240), not before_hour(${variable},21), weekday(${variable},5), weekday(${variable},6)"];


	// var rules = ['kettle(6) :- duration_gt(6, 50), start_before(6, 11), day(6, 6)',
	// 			 'kettle(6) :- duration_gt(6, 50), start_before(6, 7)'];
	var hovertexts = ['activity 6', 'the duration of activity 6 does not exceed 130 seconds', 'activity 6 starts before 10 PM',
						'activity 6', 'the duration of activity 6 does not exceed 20 seconds', 'the duration of activity 6 exceeds 0 seconds',
						'activity 6', 'activity 6 starts between 11 AM and 12 AM', 'activity 6 takes place on a friday']
	//var facts = ['duration_gt(6, 50)', 'start_before(6, 11)', 'day(6, 6)']; //, 'day 6'

	var topnode = '';
	var rule_fullfilled = 'disqualify';

	rules.forEach(function (rule, index) {
		var includes = [];
		var ruleheadbody = rule.split(" :- ");
		var part_rule_fullfilled;


		if(index == 0){
			topnode = ruleheadbody[0];
			topnode = topnode.replace('${variable}', variable)
			g.setNode(topnode, { label: topnode, shape: 'rect', class: ['none'], hovertext: 'It is plausible that activity 6 is a kettle activity'  });
			g.setNode('condor', { label: 'OR', shape: 'diamond', class: ['none'], hovertext: ''  });
		}

		bodynodes = ruleheadbody[1].split('), ');

		var qualified = 0;

		bodynodes.forEach(function(node, node_number) {
			var bodynode_fullfilled = 'disqualify';
			node = node.replace('${variable}', variable)

			if(node.slice(-1) != ')'){
				node = node + ')';
			}
			bodynodes[node_number] = node;


			for(let i = 0; i < facts.length; i++)
			{
				if(facts[i].includes(node)){
					qualified += 1;
					bodynode_fullfilled = 'qualify'
					break;
				}
			}

			includes.push(bodynode_fullfilled);

			// if(facts.includes(node)){
			// 	includes.push('qualify');
			// }else{
			// 	includes.push('disqualify');
			// 	part_rule_fullfilled = 'disqualify';
			// }
		});


		var part_rule_fullfilled = "disqualify";
		if (qualified == bodynodes.length){
			part_rule_fullfilled = "qualify";
		}

		g.setNode('condand' + index, { label: 'AND', shape: 'diamond', class: [part_rule_fullfilled], hovertext: ''  });
		g.setEdge("condand" + index, "condor",  { class: [part_rule_fullfilled], label: "", hovertext:"" });

		bodynodes.forEach(function(node, node_number) {
			g.setNode(node+index, { label: node, shape: 'rect', class: [includes[node_number]], hovertext: hovertexts[(index * 3) + node_number]  });  //style: 'fill: red'
			g.setEdge(node+index, "condand" + index,  {class: [includes[node_number]], label: "", hovertext:"" });
		});

		if(part_rule_fullfilled == "qualify"){
			rule_fullfilled = "qualify";
		}
	});

	g.setEdge("condor", topnode,  { class: [rule_fullfilled], label: "", hovertext:"" });

	var svg = d3.select("svg"),
		inner = svg.select("g");
		inner.selectAll("*").remove();
		topnode = g.node(topnode);
		topcond = g.node("condor");


	topnode.class = rule_fullfilled;
	topcond.class = rule_fullfilled;



	// Set the rankdir
	g.graph().rankdir = 'BT';//'LR';
	g.graph().nodesep = 50;

	// Set up zoom support
	var zoom = d3.zoom().on("zoom", function() {
		  inner.attr("transform", "translate(" + d3.event.translate + ")" +
									  "scale(" + d3.event.scale + ")");
		});
	svg.call(zoom);

	// Create the renderer
	var render = new dagreD3.render();




	// Run the renderer. This is what draws the final graph.
	render(inner, g);


	var tooltip = d3.select("body")
		.append("div")
		.style("position", "absolute")
		.style("background-color", "white")
	  .style("border", "solid")
	  .style("border-width", "2px")
	  .style("border-radius", "5px")
	  .style("padding", "5px")
		.style("z-index", "10")
		.style("visibility", "hidden")
		.text("Simple Tooltip...");


	inner.selectAll('g.node')
	  .attr("data-hovertext", function(v) {
			return g.node(v).hovertext
		})
		.on("mouseover", function(){if(this.dataset.hovertext != ""){return tooltip.style("visibility", "visible");}})
		.on("mousemove", function(){
		tooltip.text( this.dataset.hovertext)
			.style("top", (event.pageY-10)+"px")
			.style("left",(event.pageX+10)+"px");
	  })
		.on("mouseout", function(){return tooltip.style("visibility", "hidden");});
}

function makeList(listData) {

	activities = listData
	const checker = value =>
    ['kettle'].some(element => value.includes(element));
    listData = listData.filter(checker);
	console.log(listData);


    // Make a container element for the list
    let listContainer = document.getElementById("listContainer");

    // Set up a loop that goes through the items in listItems one at a time
    let numberOfListItems = listData.length;

    for (let i = 0; i < numberOfListItems; ++i) {

			var radiobox = document.createElement('input');
			radiobox.type = 'radio';
			radiobox.id = 'activity';
			radiobox.name = 'activity';
			radiobox.value = listData[i].split('::')[1];


			if(i == 0){
				radiobox.checked = true;
			}

			var label = document.createElement('label')
			label.htmlFor = listData[i].split('::')[1];

			var description = document.createTextNode(listData[i].split('::')[1]);
			label.appendChild(description);


			var newline = document.createElement('br');

			radiobox.addEventListener("click", () => getJSON(parseInt(listData[i].split('::')[1].split('(')[1].split(')')[0])))

			listContainer.appendChild(radiobox);
			listContainer.appendChild(label);
			listContainer.appendChild(newline);

    }
}





// Center the graph
// var initialScale = 0.75;
// zoom
//   .translate([(svg.attr("width") - g.graph().width * initialScale) / 2, 20])
//   .scale(initialScale)
//   .event(svg);
// svg.attr('height', g.graph().height * initialScale + 40);



