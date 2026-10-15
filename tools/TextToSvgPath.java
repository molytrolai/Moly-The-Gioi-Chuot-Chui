import java.awt.Font;
import java.awt.font.FontRenderContext;
import java.awt.font.GlyphVector;
import java.awt.geom.PathIterator;
import java.awt.geom.Rectangle2D;
import java.awt.Shape;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

public class TextToSvgPath {
    public static class Result {
        public String path;
        public double width;
        public double height;
    }

    public static Result getSvgPath(String text, String fontName, int fontStyle, float fontSize, boolean centerOrigin) {
        Font font = new Font(fontName, fontStyle, (int)fontSize);
        FontRenderContext frc = new FontRenderContext(null, true, true);
        GlyphVector gv = font.createGlyphVector(frc, text);
        Shape shape = gv.getOutline(0, 0);
        Rectangle2D bounds = shape.getBounds2D();
        
        double offsetX = centerOrigin ? -(bounds.getX() + bounds.getWidth() / 2.0) : 0;
        double offsetY = centerOrigin ? -(bounds.getY() + bounds.getHeight() / 2.0) : 0;

        StringBuilder sb = new StringBuilder();
        PathIterator pi = shape.getPathIterator(null);
        double[] coords = new double[6];
        
        while (!pi.isDone()) {
            int type = pi.currentSegment(coords);
            switch (type) {
                case PathIterator.SEG_MOVETO:
                    sb.append(String.format(java.util.Locale.US, "M %.2f %.2f ", coords[0] + offsetX, coords[1] + offsetY));
                    break;
                case PathIterator.SEG_LINETO:
                    sb.append(String.format(java.util.Locale.US, "L %.2f %.2f ", coords[0] + offsetX, coords[1] + offsetY));
                    break;
                case PathIterator.SEG_QUADTO:
                    sb.append(String.format(java.util.Locale.US, "Q %.2f %.2f %.2f %.2f ", 
                        coords[0] + offsetX, coords[1] + offsetY, coords[2] + offsetX, coords[3] + offsetY));
                    break;
                case PathIterator.SEG_CUBICTO:
                    sb.append(String.format(java.util.Locale.US, "C %.2f %.2f %.2f %.2f %.2f %.2f ", 
                        coords[0] + offsetX, coords[1] + offsetY, coords[2] + offsetX, coords[3] + offsetY, coords[4] + offsetX, coords[5] + offsetY));
                    break;
                case PathIterator.SEG_CLOSE:
                    sb.append("Z ");
                    break;
            }
            pi.next();
        }
        
        Result res = new Result();
        res.path = sb.toString().trim();
        res.width = bounds.getWidth();
        res.height = bounds.getHeight();
        return res;
    }

    public static void main(String[] args) throws Exception {
        // Read text from UTF-8 stdin
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        String text = reader.readLine();
        if (text == null || text.isEmpty()) {
            text = "ĐĂNG NHẬP";
        }

        String fontName = args.length > 0 ? args[0] : "Arial";
        int style = Font.BOLD;
        if (args.length > 1 && args[1].equalsIgnoreCase("plain")) {
            style = Font.PLAIN;
        }
        float size = args.length > 2 ? Float.parseFloat(args[2]) : 24f;
        boolean center = args.length <= 3 || Boolean.parseBoolean(args[3]);

        Result res = getSvgPath(text, fontName, style, size, center);
        System.out.println("BOUNDS:" + res.width + "," + res.height);
        System.out.println("PATH:" + res.path);
    }
}
