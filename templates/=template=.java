import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class %FILE%
{
    public static void main(String[] args) {
        // Read file into list of strings
        List<String> infile;
        try (Stream<String> lines = Files.lines(Paths.get(args[0]))) {
	    infile = lines.collect(Collectors.toList());
        } catch(IOException e) {
	    return;
        }

        // Read first line into list of integers
        Scanner scanner = new Scanner(infile.get(0));
        List<Integer> firstline = new ArrayList<Integer>();
        while (scanner.hasNextInt()) {
	    firstline.add(scanner.nextInt());
        }

        %HERE%
    }
}
