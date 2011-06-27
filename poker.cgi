#!/usr/bin/tclsh
######################################################################################
#                       NOTE: best viewed with tabstops = 3.
######################################################################################
#   Author: Jin Young Kim
#     Date: Tuesday, March 30, 1999
# Filename: poker hand
######################################################################################
# Vers. | Additions and Modifications Summary
#-------------------------------------------------------------------------------------
# 1.0	  |
#  	  |
######################################################################################
#  Tcl Proc: main
#* Purpose: Starts the program, decides which procedure to goto next.
######################################################################################
proc main {} {
	init_script
	global global_l
	foreach i "$global_l" {global $i}

	if {![info exists cgi_args(action)]} {
		set cgi_args(action) "printTable"
	}
	if {[regsub -all {\[} $cgi_args(action) "" action] == 0} {}
	set procname "$action"
	eval $procname
}
######################################################################################
#  Tcl Proc: init_script
#* Purpose: This initializes the script's var and other such stuff
######################################################################################
proc init_script {} {
	global global_l
	lappend global_l \
		argv0 env CGIARGS HOMEDIR HTMLDIR LOGDIR LIBDIR \
		PROGNAME VERSION CARDS_L CARDIMGDIR CURDECK HANDNAME

	foreach i "$global_l" {
		global $i
	}

	set HOMEDIR "/home/jinyk"
	set HTMLDIR "$HOMEDIR/jinyoungandyuyoun.com"
	set LOGDIR "$HOMEDIR/logs/jinyounganyuyoun.com/html"
	set LIBDIR "$HTMLDIR/cgi-bin"

	source $LIBDIR/cgi_args.tlib
	source $LIBDIR/html.tlib

	if {[info exists env(REQUEST_METHOD)]} {
		place_cgi_args CGIARGS
		foreach i [array names CGIARGS] {
			if {[regsub -all {\[} "$CGIARGS($i)" "" temp] == 0} {}
			if {[regsub -all {eval } "$CGIARGS($i)" "" temp] == 0} {}
			set CGIARGS($i) [string trim $CGIARGS($i)]
		}
	}

	set PROGNAME "Poker"
	set VERSION "1.0"
	set CARDS_L {2s 2c 2d 2h 3s 3c 3d 3h 4s 4c 4d 4h 5s 5c 5d 5h 6s 6c 6d 6h 7s 7c 7d 7h 8s 8c 8d 8h 9s 9c 9d 9h 0s 0c 0d 0h js jc jd jh qs qc qd qh ks kc kd kh as ac ad ah}
	set CARDIMGDIR "/images/cards/"
	set HANDNAME(0) "High Card"
	set HANDNAME(1) "Pair"
	set HANDNAME(2) "Two Pair"
	set HANDNAME(3) "Three of a Kind"
	set HANDNAME(4) "Straight"
	set HANDNAME(5) "Flush"
	set HANDNAME(6) "Full House"
	set HANDNAME(7) "Four of a Kind"
	set HANDNAME(8) "Straight Flush"
	set HANDNAME(9) "Royal Flush"
}
######################################################################################
#  Tcl Proc:
#* Purpose:
######################################################################################
proc printTable {} {
	global global_l
	foreach i "$global_l" {global $i}

	set CURDECK [shuffle $CARDS_L]

	for {set i 0} {$i < 7} {incr i} {
		set hand($i) [dealMe 7]
		set vHand($i) [valueHand $hand($i)]
	}

	html_begin Poker

	puts "In honor of my new found love of poker...<br>
	So far this program doesn't do much. It shuffles a 52 card deck, deals 7 cards to 7 hands,
	then figures out what each hand is worth and sorts the hands in order and names them. As
	soon as I figure out how to deal with the concept of bluffing and betting I will perhaps
	write an actual game. <i>Reload this page to deal again.</i><HR>"

	set sortedHands "0"
	for {set i 1} {$i < 7} {incr i} {
		set sortedLength [llength $sortedHands]
		for {set j 0} {$j < $sortedLength} {incr j} {
			if {[lindex $sortedHands $j] != $i} {
				if {[compareHands $vHand([lindex $sortedHands $j]) $vHand($i)] != -1} {
					set sortedHands [linsert $sortedHands $j $i]
					set j $sortedLength
				} else {
					if {[expr $j + 1] == $sortedLength} {
						lappend sortedHands $i
					}
				}
			}
		}
	}

	foreach handIdx $sortedHands {
		foreach card $hand($handIdx) {
			puts "[createCardImgStr $card]"
		}
		puts " = $HANDNAME([lindex $vHand($handIdx) 0])<BR>"
	}

	html_end
}
######################################################################################
#  Tcl Proc:
#* Purpose:
######################################################################################
proc compareHands {hand1 hand2} {
	if {[lindex $hand1 0] > [lindex $hand2 0]} {
		set returnStr -1
	} else {
		if {[lindex $hand1 0] < [lindex $hand2 0]} {
			set returnStr 1
		} else {
			if {[lindex $hand1 1] > [lindex $hand2 1]} {
				set returnStr -1
			} else {
				if {[lindex $hand1 1] < [lindex $hand2 1]} {
					set returnStr 1
				} else {
					if {[lindex $hand1 2] > [lindex $hand2 2]} {
						set returnStr -1
					} else {
						if {[lindex $hand1 2] < [lindex $hand2 2]} {
							set returnStr 1
						} else {
							set returnStr 0
						}
					}
				}
			}
		}
	}
	return $returnStr
}
######################################################################################
#  Tcl Proc:
#* Purpose:
######################################################################################
proc shuffle {deck} {
	set newDeck ""
	set deckSize [llength $deck]
	for {set i 0} {$i < $deckSize} {incr i} {
		set tempcardnum [expr int (rand() * [llength $deck])]
		lappend newDeck [lindex $deck $tempcardnum]
		set deck [lreplace $deck $tempcardnum $tempcardnum]
	}
	return $newDeck
}
######################################################################################
#  Tcl Proc:
#* Purpose:
######################################################################################
proc dealMe {numCards} {
	global global_l
	foreach i "$global_l" {global $i}

	set returnCards [lrange $CURDECK 0 [expr $numCards - 1]]
	set CURDECK [lreplace $CURDECK 0 [expr $numCards - 1]]
	return $returnCards
}
######################################################################################
#  Tcl Proc:
#* Purpose:
######################################################################################
proc valueHand {hand} {
	global global_l
	foreach i "$global_l" {global $i}

	#set noPair 0
	#set hasPair 0
	#set has2Pair 0
	set has3OfAKind 0
	set hasStraight 0
	set hasFlush 0
	set hasFullHouse 0
	#set has4OfAKind 0
	set hasStraightFlush 0
	set size1 ""
	set size2 ""
	set size3 ""
	set size4 ""

	set handLength [llength $hand]
	for {set i 0} {$i < $handLength} {incr i} {
		set curCard [lindex $hand $i]
		set card [string index $curCard 0]
		set suit [string index $curCard 1]
		switch $card {
			0 {set card 10}
			j {set card 11}
			q {set card 12}
			k {set card 13}
			a {set card 14}
		}
		lappend handValue $card
		lappend handSuit $suit
		lappend handSuitValue "$suit $card"
	}

	set handValue [lsort -integer $handValue]
	set handSuit [lsort $handSuit]

	# Check for flush and straight flush
	while {[llength $handSuit] > 0} {
		set suit [lindex $handSuit 0]
		set suit_l $suit
		set handSuit [lreplace $handSuit 0 0]
		while {1} {
			if {$suit == [lindex $handSuit 0]} {
				lappend suit_l [lindex $handSuit 0]
				set handSuit [lreplace $handSuit 0 0]
			} else {
				break
			}
		}
		if {[llength $suit_l] >= 5} {
			foreach suitValue $handSuitValue {
				if {$suit == [lindex $suitValue 0]} {
					lappend value_l [lindex $suitValue 1]
				}
			}
			set hasStraightFlush [checkStraight $value_l]
			set hasFlush "[lsort -integer $value_l]"
			break
		}
	}
	if {$hasStraightFlush == 0} {
		set tmpHandValue $handValue
		while {[llength $tmpHandValue] > 0} {
			set card [lindex $tmpHandValue 0]
			set card_l $card
			set tmpHandValue [lreplace $tmpHandValue 0 0]
			while {1} {
				if {$card == [lindex $tmpHandValue 0]} {
					lappend card_l [lindex $tmpHandValue 0]
					set tmpHandValue [lreplace $tmpHandValue 0 0]
				} else {
					break
				}
			}
			switch [llength $card_l] {
				1 {lappend size1 $card_l}
				2 {lappend size2 $card_l}
				3 {lappend size3 $card_l}
				4 {lappend size4 $card_l}
			}
		}
		set handValueSep [list $size1 $size2 $size3 $size4]

		if {[llength [lindex $handValueSep 3]] == 1} {
			set theValue "7 [lindex [lindex [lindex $handValueSep 3] 0] 0] 0"
		} else {
			if {[llength [lindex $handValueSep 2]] > 0} {
				if {[llength [lindex $handValueSep 2]] > 1} {
					set hasFullHouse [lindex [lindex [lindex $handValueSep 2] 1] 0]
				} else {
					if {[llength [lindex $handValueSep 1]] > 0} {
						set hasFullHouse [lindex [lindex [lindex $handValueSep 2] 0] 0]
					} else {
						set has3OfAKind [lindex [lindex [lindex $handValueSep 2] 0] 0]
					}
				}
			}
			if {$hasFullHouse == 0} {
				if {$hasFlush == 0} {
					# Check for Straight
					set hasStraight [checkStraight $handValue]
					if {$hasStraight == 0} {
						if {$has3OfAKind == 0} {
							if {[llength [lindex $handValueSep 1]] > 0} {
								set thePairs [lindex $handValueSep 1]
								switch [llength [lindex $handValueSep 1]] {
									1 {
										set pair1 [lindex $thePairs 0]
										set theValue "1 [lindex $pair1 0] [binRep [subtractCards $pair1 $handValue]]"
									}
									2 {
										set pair1 [lindex $thePairs 0]
										set pair2 [lindex $thePairs 1]
										set theValue "2 [binRep "[lindex $pair1 0] [lindex $pair2 0]"] [subtractCards "$pair1 $pair2" $handValue]"
									}
									3 {
										set pair1 [lindex $thePairs 1]
										set pair2 [lindex $thePairs 2]
										set theValue "2 [binRep "[lindex $pair1 0] [lindex $pair2 0]"] [subtractCards "$pair1 $pair2" $handValue]"
									}
								}
							} else {
								set theValue "0 [binRep $handValue] 0"
							}
						} else {
							set theValue "3 $has3OfAKind 0"
						}
					} else {
						set theValue "4 $hasStraight 0"
					}
				} else {
					set theValue "5 [binRep $hasFlush] 0"
				}
			} else {
				set theValue "6 $hasFullHouse 0"
			}
		}
	} else {
		#we have a straight flush!
		if {$hasStraightFlush == 14} {
			set theValue "9 0 0"
		} else {
			set theValue "8 $hasStraightFlush 0"
		}
	}
	return $theValue
}
######################################################################################
#  Tcl Proc:
#* Purpose:
######################################################################################
proc checkStraight {cardVal_l} {
	global global_l
	foreach i "$global_l" {global $i}

	set isStraight 0
	set cardVal_l [lsort -integer $cardVal_l]
	while {[llength $cardVal_l] > 0} {
		set card [lindex $cardVal_l 0]
		set cardVal_l [lreplace $cardVal_l 0 0]
		while {1} {
			if {$card == [lindex $cardVal_l 0]} {
				set cardVal_l [lreplace $cardVal_l 0 0]
			} else {
				break
			}
		}
		lappend newCardVal_l $card
	}
	set cardVal_l $newCardVal_l
	if {[llength $cardVal_l] >= 5} {
		if {[lindex $cardVal_l end] == 14} {
			set cardVal_l [linsert $cardVal_l 0 1]
		}
		for {set i 0} {$i < [expr [llength $cardVal_l] - 4]} {incr i} {
			if {([lindex $cardVal_l $i] == [expr [lindex $cardVal_l [expr $i + 1]] -1]) && \
				 ([lindex $cardVal_l $i] == [expr [lindex $cardVal_l [expr $i + 2]] -2]) && \
				 ([lindex $cardVal_l $i] == [expr [lindex $cardVal_l [expr $i + 3]] -3]) && \
				 ([lindex $cardVal_l $i] == [expr [lindex $cardVal_l [expr $i + 4]] -4])} {
				 set isStraight [lindex $cardVal_l [expr $i + 4]]
			}
		}
	}
	return $isStraight
}

######################################################################################
#  Tcl Proc:
#* Purpose:
######################################################################################
proc binRep {cards2Add} {
	set sum 0
	foreach curCard $cards2Add {
		set sum [expr int([expr $sum + [expr pow(2, [expr $curCard - 2])]])]
	}
	return $sum
}
######################################################################################
#  Tcl Proc:
#* Purpose:
######################################################################################
proc subtractCards {subCards wholeHand} {
	foreach curCard $subCards {
		regsub "$curCard " "$wholeHand " "" wholeHand
		set wholeHand [string trim $wholeHand]
	}
	set returnStr [lrange $wholeHand [expr [llength $wholeHand] - [expr 5 - [llength $subCards]]] end]
	return $returnStr
}
######################################################################################
#  Tcl Proc:
#* Purpose:
######################################################################################
proc createCardImgStr {whichCard} {
	global CARDIMGDIR

	return "<img src=\"[set CARDIMGDIR][set whichCard].gif\">"
}
######################################################################################
#  Tcl Proc:
#* Purpose:
######################################################################################
proc createBackImgStr {{numCards 1}} {
	global CARDIMGDIR

	set returnStr ""
	for {set i 0} {$i < $numCards} {incr i} {
		append returnStr "<img src=\"[set CARDIMGDIR]b.gif\">"
	}

	return $returnStr
}
######################################################################################
#  Tcl Proc: capfirstletter
#* Purpose: Capitalizes the first letter and lowercases the rest
######################################################################################
proc capfirstletter {stringtocap} {
	return "[string toupper [string index $stringtocap 0]][string tolower [string range $stringtocap 1 end]]"
}
######################################################################################
#  Tcl Proc: debug
#* Purpose: puts to std error
######################################################################################
proc debug {debug_info} {
	puts stderr $debug_info
}
######################################################################################
############################### calls the main proc ##################################
######################################################################################
main
