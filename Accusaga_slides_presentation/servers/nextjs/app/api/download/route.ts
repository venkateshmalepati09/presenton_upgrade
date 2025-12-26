
import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET(req: NextRequest) {
    const searchParams = req.nextUrl.searchParams;
    const filePath = searchParams.get("path");

    if (!filePath) {
        return NextResponse.json({ error: "No path provided" }, { status: 400 });
    }

    // Security check: ensure file exists
    if (!fs.existsSync(filePath)) {
        return NextResponse.json({ error: "File not found" }, { status: 404 });
    }

    // Security check: simple check to ensure we only serve expected file types
    const ext = path.extname(filePath).toLowerCase();
    if (ext !== ".pdf" && ext !== ".pptx") {
        return NextResponse.json({ error: "Invalid file type" }, { status: 400 });
    }

    try {
        const fileBuffer = fs.readFileSync(filePath);
        const filename = path.basename(filePath);

        // Determine content type
        let contentType = "application/octet-stream";
        if (ext === ".pdf") {
            contentType = "application/pdf";
        } else if (ext === ".pptx") {
            contentType = "application/vnd.openxmlformats-officedocument.presentationml.presentation";
        }

        return new NextResponse(fileBuffer, {
            headers: {
                "Content-Type": contentType,
                "Content-Disposition": `attachment; filename="${filename}"`,
            },
        });
    } catch (error) {
        console.error("Error serving file:", error);
        return NextResponse.json({ error: "Error serving file" }, { status: 500 });
    }
}
