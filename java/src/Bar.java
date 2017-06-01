import java.util.ArrayList;
import org.opencv.core.Mat;
import org.opencv.core.Rect;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Steven
 */
public class Bar {
    Mat img;
    Rect crop;
    ArrayList<Rect> holeRects;
    ArrayList<Mat> holeImgs;
    int barNum;
    boolean processed;
    boolean left;
    boolean right;
    private ArrayList<Double> measurements;


    public Bar() {
        img = null;
        crop = null;
        barNum = -1;
        left = false;
        right = false;
        processed = false;
    }
    
    public Bar(Mat image, int num, char leftOrRight, Rect r) {
        measurements = new ArrayList<>();
        crop = r;
        img = image;
        barNum = num;
        left = leftOrRight == 'L';
        right = leftOrRight == 'R';
        processed = false;
    }

    public boolean isProcessed() {
        return processed;
    }

    public void setProcessed(boolean processed) {
        this.processed = processed;
    }

    public boolean isLeft() {
        return left;
    }

    public void setLeft(boolean left) {
        this.left = left;
    }

    public boolean isRight() {
        return right;
    }

    public void setRight(boolean right) {
        this.right = right;
    }

    public Mat getImg() {
        return img;
    }

    public void setImg(Mat img) {
        img.copyTo(this.img);
    }

    public int getBarNum() {
        return barNum;
    }

    public void setBarNum(int barNum) {
        this.barNum = barNum;
    }
    public ArrayList<Double> getMeasurements() {
        return measurements;
    }

    public void setMeasurements(ArrayList<Double> measurements) {
        this.measurements = measurements;
    }

}
