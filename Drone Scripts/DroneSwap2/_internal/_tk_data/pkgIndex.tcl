<<<<<<< HEAD
if {![package vsatisfies [package provide Tcl] 8.6.0]} return
if {($::tcl_platform(platform) eq "unix") && ([info exists ::env(DISPLAY)]
	|| ([info exists ::argv] && ("-display" in $::argv)))} {
    package ifneeded Tk 8.6.13 [list load [file join $dir .. .. bin libtk8.6.dll]]
} else {
    package ifneeded Tk 8.6.13 [list load [file join $dir .. .. bin tk86t.dll]]
}
=======
if {![package vsatisfies [package provide Tcl] 8.6.0]} return
if {($::tcl_platform(platform) eq "unix") && ([info exists ::env(DISPLAY)]
	|| ([info exists ::argv] && ("-display" in $::argv)))} {
    package ifneeded Tk 8.6.13 [list load [file join $dir .. .. bin libtk8.6.dll]]
} else {
    package ifneeded Tk 8.6.13 [list load [file join $dir .. .. bin tk86t.dll]]
}
>>>>>>> 40912a2cf55f1eefaa18841ceace9a0288e8636a
