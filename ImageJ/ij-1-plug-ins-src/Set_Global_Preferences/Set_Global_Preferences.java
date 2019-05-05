import ij.plugin.PlugIn;
import ij.gui.GenericDialog;
import ij.IJ;
import ij.Prefs;

public class Set_Global_Preferences implements PlugIn {
	public void run(String arg) {
		GenericDialog gd = new GenericDialog("Global Preferences");
		gd.addStringField("report directory:", "/Users/jrminter/dat/report/");
		gd.addStringField("     report file:", "report.csv");
		gd.showDialog();
		
		String strReportDir = gd.getNextString();
		String strReportFile = gd.getNextString();
		
		Prefs.set("report.dir", strReportDir);
		Prefs.set("report.file", strReportFile);
		Prefs.savePreferences();
		

	}
}