
import org.opencv.core.Size;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Steven
 */
public class Setting {
    int cannyHighThresh;
    int cannyLowThresh;
    Size kernalSize;
    double gaussianSigmaX;
    double gaussianSigmaY;
    int centerDist;
    int centerThresh;
    int minRadius;
    int maxRadius;
    
    public Setting() {
        cannyHighThresh = 50;
        cannyLowThresh = 25;
        kernalSize = new Size(3,3);
        gaussianSigmaX = 1;
        gaussianSigmaY = 1;
        centerDist = 10;
        centerThresh = 20;
        minRadius = 50;
        maxRadius = 100;
    }
    
    public Setting(int highThresh, int lowThresh, int size, double sigmaX, double sigmaY, int dist, int thresh, int min, int max) {
        cannyLowThresh = lowThresh;
        cannyHighThresh = highThresh;
        kernalSize = new Size(size,size);
        gaussianSigmaX = sigmaX;
        gaussianSigmaY = sigmaY;
        centerDist = dist;
        centerThresh = thresh;
        minRadius = min;
        maxRadius = max;
    }
    
    public void copy(Setting s) {
        this.cannyHighThresh = s.cannyHighThresh;
        this.centerDist = s.centerDist;
        this.centerThresh = s.centerThresh;
        this.gaussianSigmaX = s.gaussianSigmaX;
        this.gaussianSigmaY = s.gaussianSigmaY;
        this.kernalSize = s.kernalSize;
        this.maxRadius = s.maxRadius;
        this.minRadius = s.minRadius;
    }
    
    public String toString() {
        return cannyHighThresh + "\t" + (int)kernalSize.height + "\t" + gaussianSigmaX + "\t" + gaussianSigmaY + "\t" + centerDist + "\t" + centerThresh + "\t" + minRadius + "\t" + maxRadius;
    }
    
    public int getCannyHighThresh() {
        return cannyHighThresh;
    }

    public void setCannyHighThresh(int cannyHighThresh) {
        this.cannyHighThresh = cannyHighThresh;
    }

    public Size getKernalSize() {
        return kernalSize;
    }

    public void setKernalSize(Size kernalSize) {
        this.kernalSize = kernalSize;
    }

    public double getGaussianSigmaX() {
        return gaussianSigmaX;
    }

    public void setGaussianSigmaX(double gaussianSigmaX) {
        this.gaussianSigmaX = gaussianSigmaX;
    }

    public double getGaussianSigmaY() {
        return gaussianSigmaY;
    }

    public void setGaussianSigmaY(double gaussianSigmaY) {
        this.gaussianSigmaY = gaussianSigmaY;
    }

    public int getCenterDist() {
        return centerDist;
    }

    public void setCenterDist(int centerDist) {
        this.centerDist = centerDist;
    }

    public int getCenterThresh() {
        return centerThresh;
    }

    public void setCenterThresh(int centerThresh) {
        this.centerThresh = centerThresh;
    }

    public int getMinRadius() {
        return minRadius;
    }

    public void setMinRadius(int minRadius) {
        this.minRadius = minRadius;
    }

    public int getMaxRadius() {
        return maxRadius;
    }

    public void setMaxRadius(int maxRadius) {
        this.maxRadius = maxRadius;
    }
}
