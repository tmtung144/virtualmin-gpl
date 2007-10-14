#!/usr/local/bin/perl
# Show options for upgrading or un-installing some script

require './virtual-server-lib.pl';
&ReadParse();
$d = &get_domain($in{'dom'});
&can_edit_domain($d) && &can_edit_scripts() || &error($text{'edit_ecannot'});
@got = &list_domain_scripts($d);
($sinfo) = grep { $_->{'id'} eq $in{'script'} } @got;
$script = &get_script($sinfo->{'name'});
$opts = $sinfo->{'opts'};

&ui_print_header(&domain_in($d), $text{'scripts_etitle'}, "");
print "$text{'scripts_udesc'}<p>\n";

# Show install options form
print &ui_form_start("unscript_install.cgi", "post");
print &ui_hidden("dom", $in{'dom'}),"\n";
print &ui_hidden("script", $in{'script'}),"\n";
print &ui_table_start($text{'scripts_uheader'}, undef, 2);

# Show script description
print &ui_table_row($text{'scripts_iname'}, $script->{'desc'});
print &ui_table_row($text{'scripts_iversion'},
	$script->{'vdesc'}->{$sinfo->{'version'}} || $sinfo->{'version'});

# Show install URL
if ($sinfo->{'url'}) {
	print &ui_table_row($text{'scripts_iurl'},
			    "<a href='$sinfo->{'url'}'>$sinfo->{'url'}</a>");
	}
print &ui_table_row($text{'scripts_itime'}, &make_date($sinfo->{'time'}));

# Show directory
if ($opts->{'dir'}) {
	print &ui_table_row($text{'scripts_idir'},
			    "<tt>$opts->{'dir'}</tt>");
	}

# Show DB, if we have it
($dbtype, $dbname) = split(/_/, $opts->{'db'}, 2);
if ($dbtype) {
	print &ui_table_row($text{'scripts_idb'},
		&text('scripts_idbname',
		      "edit_database.cgi?dom=$in{'dom'}&type=$dbtype&".
			"name=$dbname",
		      $text{'databases_'.$dbtype}, "<tt>$dbname</tt>"));
	}

# Show login, if we have it
if ($sinfo->{'user'}) {
	print &ui_table_row($text{'scripts_iuser'},
			    &text('scripts_ipass',"<tt>$sinfo->{'user'}</tt>",
						  "<tt>$sinfo->{'pass'}</tt>"));
	}

print &ui_table_end();

# Show un-install and upgrade buttons
print &ui_submit($text{'scripts_uok'}, "uninstall"),"\n";
@vers = sort { $a <=> $b }
	     grep { &compare_versions($_, $sinfo->{'version'}) > 0 }
		  @{$script->{'versions'}};
if (@vers) {
	print "&nbsp;&nbsp;\n";
	print &ui_submit($text{'scripts_upok'}, "upgrade"),"\n";
	print &ui_select("version", $vers[$#vers],
			 [ map { [ $_ ] } @vers ]),"\n";
	}
print &ui_form_end();

&ui_print_footer("list_scripts.cgi?dom=$in{'dom'}", $text{'scripts_return'},
		 &domain_footer_link($d));

