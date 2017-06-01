
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.ArrayList;
import java.util.List;
import javax.imageio.ImageIO;
import org.opencv.core.CvException;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfInt;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import static org.opencv.imgcodecs.Imgcodecs.CV_IMWRITE_JPEG_QUALITY;
import static org.opencv.imgcodecs.Imgcodecs.imread;
import static org.opencv.imgcodecs.Imgcodecs.imwrite;
import org.opencv.imgproc.Imgproc;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Steven
 */



public class testing {
    
    static File measurementDirectory = new File("C:\\Users\\Steven\\Desktop\\Test\\Images\\");
    
    private static ArrayList<Integer> findWhitePixel(Mat img_in, int abs_x, int abs_y) {
        Mat window = new Mat();
        img_in.copyTo(window);
        ArrayList<Integer> coord = new ArrayList<>();
        int count = 0;
        int width = window.width();
        int height = window.height();
        int x = 0;
        int y = 0;
        while (org.opencv.core.Core.countNonZero(window) > 1) {
            width = window.width();
            height = window.height();
            System.out.println("Width, Height = " + width + ", " + height);
            // Shrink the window
            switch (count % 4) {
                case 0:
                    if (width != 1) {
                        window = new Mat(window, new Rect(0, 0, width - 1, height));
                    }
                    break;
                case 1:
                    if (height != 1) {
                        window = new Mat(window, new Rect(0, 0, width, height - 1));
                    }
                    break;
                case 2:
                    if (width != 1) {
                        window = new Mat(window, new Rect(1, 0, width - 1, height));
                        x++;
                    }
                    break;
                case 4:
                    if (height != 1) {
                        window = new Mat(window, new Rect(0, 1, width, height - 1));
                        y++;
                    }
                    break;
            }
            count++;
        }
        // If we end up with no white pixels, reverse the previous move
        if (org.opencv.core.Core.countNonZero(window) == 0) {
            count--;
            switch (count % 4) {
                case 0:
                    window = new Mat(img_in, new Rect(x, y, width, height));
                    break;
                case 1:
                    window = new Mat(img_in, new Rect(x, y, width, height));
                    break;
                case 2:
                    window = new Mat(img_in, new Rect(--x, y, width + 1, height));
                    break;
                case 4:
                    window = new Mat(img_in, new Rect(x, --y, width, height + 1));
                    break;
            }
        }
        width = window.width();
        height = window.height();

        for (x = 0; x < width; x++) {
            for (y = 0; y < height; y++) {
                if (window.get(y, x)[0] == 255.) {
                    coord.add(abs_x + x + 4);
                    coord.add(abs_y + y);
                }
            }
        }
        return coord;
    }
    
    private static ArrayList<Double> fitCircleSimple(Mat circle, Setting setting, int xOff, int yOff) {
        System.out.println("Fitting circle with setting: " + setting.toString());
        ArrayList<Double> retMeasurements = new ArrayList<>(4);
        // Make an edge image of the circle
        Mat blurred = new Mat(circle.width(), circle.height(), circle.type());
        Imgproc.GaussianBlur(circle, blurred, setting.kernalSize,setting.gaussianSigmaX, setting.gaussianSigmaY);
        Mat edges = new Mat(blurred.width(), blurred.height(), blurred.type());
        Imgproc.Canny(blurred, edges, setting.cannyLowThresh, setting.cannyHighThresh);
        
        // Find a radius for the circle
        double average_center_x = 0;
	double average_center_y = 0;
	double average_radius = 0;
	int h = edges.height();
        int w = edges.width();
	int prev_x_step = 0;
        int prev_y_step = 0;
	int counts = 0;
        int samples = 10;
        for (int n = 0; n < samples; n++) {
                System.out.println("Sample number: " + n);
                // Start in the center of the circle
		int y = h / 2;
		int x = w / 2;
                double x_step_double = 1. - (double) n / (samples - 1);
		double y_step_double = (double) n / (samples - 1);
//                System.out.println("Computed (x_step, y_step): (" + x_step_double + ", " + y_step_double + ")");
		double min_step = (x_step_double < y_step_double ? x_step_double : y_step_double);
                double scaling = 0;
		if (min_step != 0) {
			scaling = 1/min_step;
                } else {
			scaling = 1;
                }
		int x_step = (int) Math.round(x_step_double * scaling);
		int y_step = (int) Math.round(y_step_double * scaling);
		System.out.println("Scaled: (" + x_step + "," + y_step + ")");
		if ((x_step == prev_x_step) && (y_step == prev_y_step)) {
                    continue;
                } else {
                    prev_x_step = x_step;
                    prev_y_step = y_step;
                }
                ArrayList<Integer> white_pixel_coord = new ArrayList<>();
		while (true) {
			x += x_step;
			y += y_step;
                        // If the boundary of the image was passed, stop the loop
			if (x >= w || y >= h || x < 0 || y < 0) {
				System.out.println("Out of bounds: (" + x + "," + y + ")");
				break;
                        }
			// Look in the region just passed for white pixels
                        Rect window_box = new Rect(x - x_step, y - y_step, x_step + 1, y_step + 1);
                        Mat window = new Mat(edges, window_box);
                        // If a white pixel was passed, stop the loop
			if (org.opencv.core.Core.countNonZero(window) != 0) {
                                white_pixel_coord = findWhitePixel(window, x - x_step, y - y_step);
                                System.out.println("Found white pixel at (" + white_pixel_coord.get(0) + ", " + white_pixel_coord.get(1) +")");
				break;
                        }
                }
		if (x >= w || y >= h || x < 0 || y < 0) {
			continue;
                }
                                
		int right = x - x_step / 2;
		int bottom = y - y_step / 2;

                right = white_pixel_coord.get(0);
                bottom = white_pixel_coord.get(1);
                
                System.out.println("Right: " + right + " Bottom: " + bottom);
                
		y = h / 2;
		x = w / 2;
                while (true) {
			x -= x_step;
			y -= y_step;
                        // If the boundary of the image was passed, stop the loop
			if (x >= w || y >= h || x < 0 || y < 0) {
				System.out.println("Out of bounds: (" + x + "," + y + ")");
				break;
                        }
			// Look in the region just passed for white pixels
                        Rect window_box = new Rect(x, y, x_step + 1, y_step + 1);
                        Mat window = new Mat(edges, window_box);
                        // If a white pixel was passed, stop the loop
			if (org.opencv.core.Core.countNonZero(window) != 0) {
                                white_pixel_coord = findWhitePixel(window, x, y);
                                System.out.println("Found white pixel at (" + white_pixel_coord.get(0) + ", " + white_pixel_coord.get(1) +")");
				break;
                        }
                }
                
		if (x >= w || y >= h || x < 0 || y < 0) {
			continue;
                }
                
		int left = x + x_step / 2;
		int top = y + y_step / 2;

                left = white_pixel_coord.get(0);
                top = white_pixel_coord.get(1);
                
                System.out.println("Left: " + left + " Top: " + top);
                
                double center_x = (right + left) / 2;
		double center_y = (top + bottom) / 2;
                if ((x_step == 1 && y_step == 0) || (x_step == 0 && y_step == 1)) {
                    average_center_x += center_x;
                    average_center_y += center_y;
                }

		double radius = Math.sqrt(Math.pow(right - center_x, 2) + Math.pow(top - center_y, 2));
		System.out.println("Radius: " + radius);
		average_radius += radius;
		counts += 1;
        }
	if (counts == 0) {
            System.out.println("No circles found in bar!");
            retMeasurements.add(-1.);
            retMeasurements.add(-1.);
            retMeasurements.add(-1.);
            retMeasurements.add(-1.);
            return retMeasurements;
        }
	average_center_x = average_center_x / 2;
	average_center_y = average_center_y / 2;
	average_radius /= counts;
        
        System.out.println("Found circle with center (" + average_center_x + ", " + average_center_y + ") and radius " + average_radius);
        
        retMeasurements.add(average_center_x + xOff);
        retMeasurements.add(average_center_y + yOff);
        retMeasurements.add(average_radius);
        retMeasurements.add(-1.);
        
        File out;
        File out_draw;
        for (int j = 0;; j++) {
            out = new File(measurementDirectory, "Hole_" + j + "_edges" + ".jpg");
            if (!out.exists()) break;
        }
        for (int j = 0;; j++) {
            out_draw = new File(measurementDirectory, "Hole_" + j + "_draw" + ".jpg");
            if (!out_draw.exists()) break;
        }
        imwrite(out.toString(), edges);
        // Print the found circle onto the original image and save the image to disk
        BufferedImage img = CV.matToBufferedImage(edges, null);
        BufferedImage imgRGB = new BufferedImage(img.getWidth(), img.getHeight(), BufferedImage.TYPE_3BYTE_BGR);
        imgRGB.getGraphics().drawImage(img, 0, 0, null);
        Graphics2D g = imgRGB.createGraphics();
        g.setColor(Color.red);
        g.setStroke(new BasicStroke(1));
        int radius = (int) average_radius;
        g.drawOval((int) Math.round(average_center_x - radius), (int) Math.round(average_center_y - radius), 2*radius, 2*radius);
        g.dispose();
        try {
            ImageIO.write(imgRGB, "jpg", out_draw);
        } catch (Exception e) {
            System.out.println(e);
        }
        return retMeasurements;
    }
    
    private static void fitCircleContourAreas(Mat circle, Setting setting, int xOff, int yOff, int bar_num) {
        System.out.println("Fitting circle with setting: " + setting.toString());
        ArrayList<Double> retMeasurements = new ArrayList<>(4);
        // Make an edge image of the circle
        
        Mat blurred = new Mat(circle.width(), circle.height(), circle.type());
        Imgproc.GaussianBlur(circle, blurred, setting.kernalSize,setting.gaussianSigmaX, setting.gaussianSigmaY);
        Mat edges = new Mat(blurred.width(), blurred.height(), blurred.type());
        Imgproc.Canny(blurred, edges, setting.cannyLowThresh, setting.cannyHighThresh);
        
        Mat wider_edges = new Mat();
        Mat se = Imgproc.getStructuringElement(Imgproc.MORPH_DILATE, new Size(2, 2));
        Imgproc.dilate(edges, wider_edges, se);
        imwrite("C:\\Users\\Steven\\Desktop\\Test\\Images\\dilated.jpg", wider_edges);
        
        List<MatOfPoint> contours = new ArrayList<>();
        Imgproc.findContours(edges.clone(), contours, new Mat(), Imgproc.RETR_LIST, Imgproc.CHAIN_APPROX_SIMPLE);
        System.out.println("Found " + contours.size() + " contours.");
        double min_area = Math.PI * 225 * 225;
        double max_area = Math.PI * 235 * 235;
        
        int largest = 0;
        int second_largest = 0;
        
        double largest_area = 0;
        for (int i = 0; i < contours.size(); i++) {
            double area = Imgproc.contourArea(contours.get(i));
            if (area > max_area) {
                largest_area = area;
                largest = i;
            }
        }
        
        double second_largest_area = 0;
        for (int i = 0; i < contours.size(); i++) {
            double area = Imgproc.contourArea(contours.get(i));
            if (area > second_largest_area && area < max_area) {
                second_largest_area = area;
                second_largest = i;
            }
        }
        
        Mat draw = new Mat();
        Imgproc.cvtColor(edges, draw, Imgproc.COLOR_GRAY2BGR);
        Imgproc.drawContours(draw, contours, -1, new Scalar(0, 255, 0));
        imwrite("C:\\Users\\Steven\\Desktop\\Test\\Images\\contours_all.jpg", draw);

        if (largest_area > min_area && largest_area < max_area) {
            double radius = Math.sqrt(largest_area) / Math.PI;
            
        }
        
        for (int i = 0; i < contours.size(); i++) {
            draw = new Mat();
            Imgproc.cvtColor(edges, draw, Imgproc.COLOR_GRAY2BGR);
            Imgproc.drawContours(draw, contours, i, new Scalar(0, 255, 0));
            imwrite("C:\\Users\\Steven\\Desktop\\Test\\Images\\contours_" + i + ".jpg", draw);
            if (i == largest || i == second_largest) {
                double area = Imgproc.contourArea(contours.get(i));
                System.out.println("Computed area for contour " + i + " of " + area);
                float[] radius = new float[1];
                Point center = new Point();
                Imgproc.minEnclosingCircle(new MatOfPoint2f(contours.get(i).toArray()), center, radius);
                System.out.println("Found circle with center (" + center.x + ", " + center.y + ") and radius " + radius[0]);
                draw = new Mat();
                Imgproc.cvtColor(edges, draw, Imgproc.COLOR_GRAY2BGR);
                Imgproc.circle(draw, center, (int) radius[0], new Scalar(0, 255, 0));
                imwrite("C:\\Users\\Steven\\Desktop\\Test\\Images\\contours_" + i + ".jpg", draw);
            }
        }

    }

    private static void fitCirclesMinEclosingCircle(Mat circle, Setting setting, int xOff, int yOff) {
        System.out.println("Fitting circle with setting: " + setting.toString());
        ArrayList<Double> retMeasurements = new ArrayList<>(4);
        // Make an edge image of the circle
        
        Mat blurred = new Mat(circle.width(), circle.height(), circle.type());
        Imgproc.GaussianBlur(circle, blurred, setting.kernalSize,setting.gaussianSigmaX, setting.gaussianSigmaY);
        Mat edges = new Mat(blurred.width(), blurred.height(), blurred.type());
        Imgproc.Canny(blurred, edges, setting.cannyLowThresh, setting.cannyHighThresh);
        
        Mat wider_edges = new Mat();
        Mat se = Imgproc.getStructuringElement(Imgproc.MORPH_DILATE, new Size(2, 2));
        Imgproc.dilate(edges, wider_edges, se);
        imwrite("C:\\Users\\Steven\\Desktop\\Test\\Images\\dilated.jpg", wider_edges);
        
        List<MatOfPoint> contours = new ArrayList<>();
        Imgproc.findContours(edges.clone(), contours, new Mat(), Imgproc.RETR_LIST, Imgproc.CHAIN_APPROX_SIMPLE);
        System.out.println("Found " + contours.size() + " contours.");
        double minArea = 2. * Math.PI * 225;
        double maxArea = 2. * Math.PI * 235;
        int largest = 0;
        int second_largest = 0;
        double max_area = 0;
        for (int i = 0; i < contours.size(); i++) {
            double area = Imgproc.contourArea(contours.get(i));
            if (area > max_area) {
                max_area = area;
                largest = i;
            }
        }
        double second_max_area = 0;
        for (int i = 0; i < contours.size(); i++) {
            double area = Imgproc.contourArea(contours.get(i));
            if (area > second_max_area && area < max_area) {
                second_max_area = area;
                second_largest = i;
            }
        }
        Mat draw = new Mat();
        Imgproc.cvtColor(edges, draw, Imgproc.COLOR_GRAY2BGR);
        Imgproc.drawContours(draw, contours, -1, new Scalar(0, 255, 0));
        imwrite("C:\\Users\\Steven\\Desktop\\Test\\Images\\contours_all.jpg", draw);

        for (int i = 0; i < contours.size(); i++) {
            draw = new Mat();
            Imgproc.cvtColor(edges, draw, Imgproc.COLOR_GRAY2BGR);
            Imgproc.drawContours(draw, contours, i, new Scalar(0, 255, 0));
            imwrite("C:\\Users\\Steven\\Desktop\\Test\\Images\\contours_" + i + ".jpg", draw);
            if (i == largest || i == second_largest) {
                double area = Imgproc.contourArea(contours.get(i));
                System.out.println("Computed area for contour " + i + " of " + area);
                float[] radius = new float[1];
                Point center = new Point();
                Imgproc.minEnclosingCircle(new MatOfPoint2f(contours.get(i).toArray()), center, radius);
                System.out.println("Found circle with center (" + center.x + ", " + center.y + ") and radius " + radius[0]);
                draw = new Mat();
                Imgproc.cvtColor(edges, draw, Imgproc.COLOR_GRAY2BGR);
                Imgproc.circle(draw, center, (int) radius[0], new Scalar(0, 255, 0));
                imwrite("C:\\Users\\Steven\\Desktop\\Test\\Images\\contours_" + i + ".jpg", draw);
            }
        }
    }    
    
    private static ArrayList<Double> fitCircle(Mat imgIn, Setting setting, int xOff, int yOff, int bar_num) {
//        System.out.println("Fitting circle with setting: " + setting.toString());
        ArrayList<Double> retMeasurements = new ArrayList<>(4);
        
        Mat blurred = new Mat(imgIn.cols(),imgIn.rows(),imgIn.type());
        Imgproc.GaussianBlur(imgIn, blurred, setting.getKernalSize(), setting.getGaussianSigmaX(), setting.getGaussianSigmaY());
        
        Mat edges = new Mat(blurred.width(), blurred.height(), blurred.type());
        Imgproc.Canny(blurred, edges, setting.cannyLowThresh, setting.cannyHighThresh);
        
        Mat circles = new Mat();
        Imgproc.HoughCircles(edges, circles, Imgproc.CV_HOUGH_GRADIENT, 1, setting.centerDist, setting.cannyHighThresh, setting.centerThresh, setting.minRadius, setting.maxRadius);
  
        System.out.println("Circles: " + circles.dump());
        int index = 0;
        double minRad = Double.MAX_VALUE;
        int limit = circles.width();
        for (int j = 0; j < limit; j++) {
            if (circles.get(0,j)[2] < minRad) {
                minRad = circles.get(0,j)[2];
                index = j;
            }
        }
        System.out.println("Found circle: (" + circles.get(0,index)[0] + ", " + circles.get(0,index)[1] + ") with radius " + circles.get(0,index)[2]);
//        File out;
//        for (int j = 0;; j++) {
//                out = new File(measurementDirectory + "\\BarHoles\\" + (FGB ? "FGB" : "SMB") + "_" + bar_num + "\\", "Hole_" + j + "_edges" + ".jpg");
//                if (!out.exists()) break;
//        }
//        if (circles.width() == 0) {
//            System.out.println("No circles found in bar! Trying simple method");
//            retMeasurements = fitCircleContours(imgIn, setting, xOff, yOff, bar_num);
////            retMeasurements.add(-1.);
////            retMeasurements.add(-1.);
////            retMeasurements.add(-1.);
////            retMeasurements.add(-1.);
//        } else {
////            System.out.println("Found a circle, adding to measurements.");
//            double center_x = circles.get(0, index)[0];
//            double center_y = circles.get(0, index)[1];
//            double radius = circles.get(0, index)[2];
//            retMeasurements.add(center_x + xOff);
//            retMeasurements.add(center_y + yOff);
//            retMeasurements.add(radius);
//            retMeasurements.add(-1.);
//            File out_draw;
//            for (int j = 0;; j++) {
//                out_draw = new File(measurementDirectory + "\\BarHoles\\" + (FGB ? "FGB" : "SMB") + "_" + bar_num + "\\", "Hole_" + j + "_draw" + ".jpg");
//                if (!out_draw.exists()) break;
//            }
//            Imgproc.Canny(blurred, edges, setting.cannyLowThresh, setting.cannyHighThresh);
//            drawCircleOnImageAndSave(imgIn, out_draw, (int) Math.round(center_x), (int) Math.round(center_y), (int) Math.round(radius));
//        }
//        imwrite(out.toString(), edges);
        return retMeasurements;
    }

    
    public static void main(String[] args) {
        System.loadLibrary(org.opencv.core.Core.NATIVE_LIBRARY_NAME);
        File f = new File("C:\\Users\\Steven\\Desktop\\Test\\Images\\","Frame.jpg");
        Mat fullImage = imread(f.toString(),CvType.CV_8UC1);
        Mat circle = new Mat(fullImage, new Rect(736, 1400, 600, 600));
        Mat circle_2 = new Mat(fullImage, new Rect(10950, 1350, 550, 550));
        File out = new File("C:\\Users\\Steven\\Desktop\\Test\\Images\\", "circle.jpg");
        imwrite(out.toString(), circle_2);
        Setting circle_setting = new Setting(200, 100, 3, 3, 3, 3, 100, 475, 525);
//        ArrayList<Double> measurements = fitCircleSimple(circle, circle_setting, 0, 0);
        fitCircle(circle, circle_setting, 0, 0, 1);
    }
}
