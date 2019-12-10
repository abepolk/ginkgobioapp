window.onload = update;

function update () {
  // let form = document.getElementById("seqForm");
  // false may be a string here, not a boolean
  console.log(validation_throws);
  if (validation_throws) {
    const para8 = document.createElement("p");
    const para8_text = document.createTextNode("Only A, C, G, and T are allowed in the sequence.");
    para8.appendChild(para8_text);
    document.documentElement.appendChild(para8);
  } else if (is_post) {
    if (result_found) {
      const para1 = document.createElement("p");
      const para1_text = document.createTextNode("Sequence found in protein: ".concat(protein_name));
      para1.appendChild(para1_text);
      const para2 = document.createElement("p");
      const para2_text = document.createTextNode("Location on protein: Base pair ".concat(protein_index));
      para2.appendChild(para2_text);
      document.documentElement.appendChild(para1);
      document.documentElement.appendChild(para2);
    } else {
      const para3 = document.createElement("p");
      const para3_text = document.createTextNode("Sequence not found");
      para3.appendChild(para3_text);
      document.documentElement.appendChild(para3);
    }
    if (previous_searches.number_searches !== 0) {
      const para4 = document.createElement("p");
      const para4_text = document.createTextNode("Previous searches");
      para4.appendChild(para4_text);
      document.documentElement.appendChild(para4);
      ul = document.createElement("ul");
      for (i = 0; i <= previous_searches.number_searches; i++) {
        let li5 = document.createElement("li");
        let li5_text = document.createTextNode("Sequence: ".concat(previous_searches[i][0]));
        li5.appendChild(li5_text);
        let li6 = document.createElement("li");
        let li6_text = document.createTextNode("Protein: ".concat(previous_searches[i][1]));
        li6.appendChild(li6_text);
        let li7 = document.createElement("li");
        let li7_text = document.createTextNode("Location on protein: ".concat(previous_searches[i][2]));
        li5.appendChild(li7_text);
        ul.appendChild(li5);
        ul.appendChild(li6);
        ul.appendChild(li7);
      }
    }
  }
}
  
  