import java.sql.*;
import java.util.HashSet;
import java.util.ArrayList;
import java.util.Collections;

public class MetaData 
{
	static String dataTypeName(int i) {
		switch (i) {
			case java.sql.Types.INTEGER: return "Integer";
			case java.sql.Types.REAL: return "Real";
			case java.sql.Types.VARCHAR: return "Varchar";
			case java.sql.Types.TIMESTAMP: return "Timestamp";
			case java.sql.Types.DATE: return "Date";
		}
		return "Other";
	}
	public static void executeMetadata(String databaseName) {
		/************* 
		 * Add you code to connect to the database and print out the metadta for the database databaseName. 
		 ************/
	}

	public static void main(String[] argv) {
		executeMetadata(argv[0]);
	}
}
