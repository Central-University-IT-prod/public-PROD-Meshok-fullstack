<script lang="ts" setup>
import { jsPDF } from "jspdf";
import QRCode from "qrcode-vue3";
import type { User } from "~/types/user";

const userInfo = useState<User>("g_user_info");

const generatePDF = async () => {
    const QRCode = document.querySelector(
        ".qr-component .code img"
    ) as HTMLImageElement | null;
    if (QRCode) {
        const doc = new jsPDF();

        const myFont = (await $fetch("/PDFFont.txt")) as string;

        // добавить шрифт
        doc.addFileToVFS("Raleway.ttf", myFont);
        doc.addFont("Raleway.ttf", "Raleway", "normal");
        doc.setFont("Raleway");

        doc.setFontSize(40);
        doc.text("Feedbacker", 65, 25);
        doc.addImage(QRCode, "PNG", 55, 35, 100, 100);
        doc.text(userInfo.value.name, 10, 200);
        doc.setFontSize(20);
        doc.text(`ID: ${userInfo.value.id}`, 10, 225);
        // Download file
        doc.save(`${userInfo.value.name}.pdf`);
    }
};

const downloadPNG = () => {
    const QRButton = document.querySelector(
        ".qr-component .download-button"
    ) as HTMLImageElement | null;
    if (QRButton) {
        QRButton.click();
    }
};
</script>

<template>
    <div class="qr-component flex flex-col items-center gap-2">
        <QRCode
            :width="200"
            :height="200"
            :value="$attrs.value as string"
            :qrOptions="{
                typeNumber: 0,
                mode: 'Byte',
                errorCorrectionLevel: 'H',
            }"
            :imageOptions="{
                hideBackgroundDots: true,
                imageSize: 0.4,
                margin: 0,
            }"
            :dotsOptions="{
                type: 'rounded',
            }"
            :cornersSquareOptions="{ type: 'dot', color: '#000000' }"
            :cornersDotOptions="{ type: undefined, color: '#000000' }"
            fileExt="png"
            myclass="code"
            :download="true"
            downloadButton="download-button"
            :downloadOptions="{ name: userInfo.name, extension: 'png' }"
        />
        <UBadge variant="subtle" class="flex gap-2"
            >Кликни чтобы скачать QR код организации

            <UButton
                @click="downloadPNG"
                label="PNG"
                size="2xs"
                variant="outline"
            />
            <UButton
                @click="generatePDF"
                label="PDF"
                size="2xs"
                variant="outline"
            />
        </UBadge>
    </div>
</template>

<style lang="scss">
.qr-component {
    width: fit-content;
    .code {
        border-radius: 1.5rem;
        overflow: hidden;
        padding: 8px;
        background-color: white;
    }
    > div {
        position: relative;
        .download-button {
            position: absolute;
            inset: 0;
            opacity: 0;
        }
    }
}
</style>
