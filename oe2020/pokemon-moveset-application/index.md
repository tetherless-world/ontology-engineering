---
layout: default
title: About
---

## Pokemon-Moveset-Application Team
Mitchell Falkow, Jay Franklin, Zhepeng Luo, John Slowik

## Abstract
As games become increasingly complicated, professional gamers and their audience are faced with a growing amount of information they need to understand and navigate to intelligently participate and compete.  In most cases, players simply memorize these facts and navigate them by intuition and trial-and-error, resulting in potentially large time costs to answer questions about new styles of play.  A technique for efficiently encoding the multiple layers of complexity and available information is absent; such a tool could greatly improve the accessibility of complex games for both veteran and novice players. Ontologies encode, relate, and can reason on abstract information (which can be changing, versioned, and distributed); as such, they fit these requirements perfectly.  Here, we demonstrate this on the Pokémon franchise: it has a healthy esports community, and there is a particular problem involving relatively simple mechanics that is greatly complicated by the scale of the game: teaching a specific Pokémon a specific move.  Although our technique can answer a number sub-questions players may find useful, this specific task requires players to memorize, minimally, hundreds of unique Pokémon, hundreds of unique moves, which Pokémon can learn which moves, and then navigate this information in its entirety to find a solution.

## A Super Breif Introduction to Pokémon
Pokémon is a turn based role-playing game where the player collects creatures, called Pokémon.  The primary gameplay involves Pokémon battling, wherein two Pokémon take turns using moves to inflict damage or status effects on each other.  Players can carry up to six Pokémon, though they can - and almost always - do have many more stored elsewhere. Pokémon can know at most four moves, which are determined by a number of factors, and change as the player adventures through the game. For example, a Pokémon's level, a measure that reflects and increases with a Pokémon's general power; when a Pokémon acheives certain levels, they can learn specific moves.  The specific level and move a Pokémon learns varys from species to species.

Pokémon is a Nintendo game franchise that dates back to 1996, and has since seen the release of dozens of games following the same core gameplay from above.  It is broadly considered to be one of the most successful gaming franchise ever, and unsurprisingly has developed a large community of fans that hold tournaments where players battle each other and events where players generally share their enthusiasm for the games.  

The primary appeal of the game is a combination of adventure/role-playing elements, intuitive rock-paper-scissors battling mechanics, and collect-'em-all features; the accessibility and cohesion of these features has garnerd the game's large audience, in tandem with excellent management by the game's developing studio, Nintendo, who regularly released new games that added new Pokémon and mechanics while keeping the core gameplay intact, and held public relations events and sponsorships with other groups.

## Project Pertinant Details

## Project Overview Diagram
This section will provide an overview on how an application leveraging Pokemon Moveset Ontology would provide solution to the user. 
The diagram below describes the architecture of the application.  The system in the current work is limited greatly in scope from the below.  A working framework for the ontology has been deployed and tested; however, it only handles a few Pokémon, Moves, and Items - sufficient to demonstrate all the core functionality. The user interface, system backend, and connection with external databases was cut from the project scope.
<img src="images/SystemArchitecture.png" width="100%">

## Definitions

## List of Resources

- [Ontology](ontology.md)

- [Term List](termlist.md)

- [Use Case and Competency Questions](usecase.md)

- [Demonstrations](demo.md)

- [Presentations](presentations.md)

## Acknowledgements
The project team would like to thank professors Deborah McGuinness and Elisa Kendal for their continuing technical support and guidance on the project. Additionally, the team appreaciates all of Sabbir Rashid’s and Shruthi Chari’s feedback on the artifacts and advice on the query.
