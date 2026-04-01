/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

class SketchPadField extends Component {
    static template = "fleet_rental_contracts.SketchPadField";
    static props = {
        ...standardFieldProps,
        imageFieldName: { type: String, optional: true },
    };
    static defaultProps = {
        imageFieldName: "",
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.state = useState({
            isDrawing: false,
            color: "#000000",
            lineWidth: 3,
            tool: "pen",
        });
        this._lastX = 0;
        this._lastY = 0;

        onMounted(() => {
            this._initCanvas();
        });
    }

    _initCanvas() {
        const canvas = this.canvasRef.el;
        if (!canvas) return;
        this._ctx = canvas.getContext("2d");
        const svgData = this.props.record.data[this.props.name];
        if (svgData) {
            const img = new Image();
            img.onload = () => { this._ctx.drawImage(img, 0, 0); };
            img.src = "data:image/svg+xml;base64," + btoa(svgData);
        }
        this._ctx.lineCap = "round";
        this._ctx.lineJoin = "round";
    }

    _getPos(e) {
        const canvas = this.canvasRef.el;
        const rect = canvas.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        return {
            x: (clientX - rect.left) * (canvas.width / rect.width),
            y: (clientY - rect.top) * (canvas.height / rect.height),
        };
    }

    onMouseDown(e) {
        e.preventDefault();
        const pos = this._getPos(e);
        this.state.isDrawing = true;
        this._lastX = pos.x;
        this._lastY = pos.y;
        this._ctx.beginPath();
        this._ctx.arc(pos.x, pos.y, this.state.lineWidth / 2, 0, Math.PI * 2);
        this._ctx.fillStyle = this.state.tool === "eraser" ? "#ffffff" : this.state.color;
        this._ctx.fill();
    }

    onMouseMove(e) {
        e.preventDefault();
        if (!this.state.isDrawing) return;
        const pos = this._getPos(e);
        const ctx = this._ctx;
        ctx.beginPath();
        ctx.moveTo(this._lastX, this._lastY);
        ctx.lineTo(pos.x, pos.y);
        ctx.strokeStyle = this.state.tool === "eraser" ? "#ffffff" : this.state.color;
        ctx.lineWidth = this.state.tool === "eraser" ? this.state.lineWidth * 4 : this.state.lineWidth;
        ctx.stroke();
        this._lastX = pos.x;
        this._lastY = pos.y;
    }

    onMouseUp(e) {
        if (!this.state.isDrawing) return;
        this.state.isDrawing = false;
        this._saveSketch();
    }

    _saveSketch() {
        const canvas = this.canvasRef.el;
        if (!canvas) return;
        const pngDataUrl = canvas.toDataURL("image/png");
        const pngBase64 = pngDataUrl.split(",")[1];
        const svgText =
            `<svg xmlns="http://www.w3.org/2000/svg" width="${canvas.width}" height="${canvas.height}">` +
            `<image href="${pngDataUrl}" width="${canvas.width}" height="${canvas.height}"/>` +
            `</svg>`;
        const updates = { [this.props.name]: svgText };
        if (this.props.imageFieldName) {
            updates[this.props.imageFieldName] = pngBase64;
        }
        this.props.record.update(updates);
    }

    onClear() {
        const canvas = this.canvasRef.el;
        this._ctx.clearRect(0, 0, canvas.width, canvas.height);
        this._ctx.fillStyle = "#ffffff";
        this._ctx.fillRect(0, 0, canvas.width, canvas.height);
        this._saveSketch();
    }

    onColorChange(e) { this.state.color = e.target.value; }
    onLineWidthChange(e) { this.state.lineWidth = parseInt(e.target.value); }
    setTool(tool) { this.state.tool = tool; }
}

registry.category("fields").add("sketch_pad", {
    component: SketchPadField,
    displayName: "Sketch Pad",
    supportedTypes: ["text"],
});

export default SketchPadField;
