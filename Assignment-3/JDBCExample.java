import java.sql.*;

public class JDBCExample 
{

        public static void main(String[] argv) {
                // Load the PostgreSQL JDBC Driver
                System.out.println("-------- PostgreSQL " + "JDBC Connection Testing ------------");
                try {
                        Class.forName("org.postgresql.Driver");
                } catch (ClassNotFoundException e) {
                        System.out.println("Where is your PostgreSQL JDBC Driver? " + "Include in your library path!");
                        e.printStackTrace();
                        return;
                }
                System.out.println("PostgreSQL JDBC Driver Registered!");

                // Set up the connection
                Connection connection = null;
                try {
                        connection = DriverManager.getConnection("jdbc:postgresql://localhost:5432/stackexchange","root", "root");
                } catch (SQLException e) {
                        System.out.println("Connection Failed! Check output console");
                        e.printStackTrace();
                        return;
                }

                if (connection != null) {
                        System.out.println("You made it, take control your database now!");
                } else {
                        System.out.println("Failed to make connection!");
                        return;
                }

                // Run a query and print out the results by iterating through the resultset
                Statement stmt = null;
                String query = "select * from users limit 10;";
                try {
                        stmt = connection.createStatement();
                        ResultSet rs = stmt.executeQuery(query);
                        while (rs.next()) {
                                String name = rs.getString("displayname");
                                System.out.println(name + "\t");
                        }
                        stmt.close();
                } catch (SQLException e ) {
                        System.out.println(e);
                }
        }
}
