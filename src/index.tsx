import {
  ButtonItem,
  PanelSection,
  PanelSectionRow,
  staticClasses,
  TextField,
  ToggleField
} from "@decky/ui";
import {
  callable,
  addEventListener,
  removeEventListener,
  toaster,
  definePlugin,
  // routerHook
} from "@decky/api"
import { useEffect, useState } from "react";
import { FaCheckCircle, FaNetworkWired } from "react-icons/fa";

const start = callable<[], number>("start");
const stop = callable<[], void>("stop");
const getStatus = callable<[], number>("getStatus");

const setSettings = callable<[string, string, boolean], void>("setSettings");
const getSettings = callable<[], [string, string, boolean]>("getSettings");

function Content() {
  const [spoofDpiPid, setSpoofDpiPid] = useState<number | undefined>();
  const [spoofDpiPort, setSpoofDpiPort] = useState<string>("9696");
  const [useDoh, setUseDoh] = useState<boolean>(false);
  const [spoofDpiDns, setSpoofDpiDns] = useState<string>("8.8.8.8");

  const onToggleSpoofDPI = async () => {
    console.log("Toggle SpoofDPI")

    if (spoofDpiPid) {
      await stop();
      setSpoofDpiPid(undefined);
    } else {
      const pid = await start();
      setSpoofDpiPid(pid);
      console.log("Started SpoofDPI with PID: " + pid);
    };
  };

  useEffect(() => {
    getSettings().then(([dns, port, useDoh]) => {
      setSpoofDpiDns(dns);
      setSpoofDpiPort(port);
      setUseDoh(useDoh);
    });
  }, []);

  getStatus().then((pid) => {
    setSpoofDpiPid(pid);
  });


  const setSpoofDpiConfig = async () => {
    await setSettings(spoofDpiDns, spoofDpiPort, useDoh);
  };

  return (
    <PanelSection title="SpoofDPI Control">
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={onToggleSpoofDPI}
        >
          {spoofDpiPid ? "Stop SpoofDPI" : "Start SpoofDPI"}
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        {spoofDpiPid && (
          <div style={{ display: "flex", alignItems: "center" }}>
            <FaCheckCircle style={{ color: "green", marginRight: "8px" }} />
            <p style={{ color: "green" }}>{"SpoofDPI is running with PID: " + spoofDpiPid}</p>
          </div>
        )}
      </PanelSectionRow>

      <div className={staticClasses.PanelSectionTitle}>Settings</div>
      <PanelSectionRow>
        <ToggleField
          label="Use DoH"
          checked={useDoh}
          onChange={e => setUseDoh(e.valueOf())}
        />

        <TextField
          label="DNS Server"
          value={spoofDpiDns}
          onChange={e => setSpoofDpiDns(e.target.value)}
        />

        <TextField
          label="Port"
          value={spoofDpiPort}
          onChange={e => setSpoofDpiPort(e.target.value)}
        />

        <ButtonItem
          layout="below"
          onClick={setSpoofDpiConfig}
        >
          Apply Settings
        </ButtonItem>
      </PanelSectionRow>
    </PanelSection>
  );
};

export default definePlugin(() => {
  const restartListener = addEventListener<[]>("decky_spoof_dpi_needs_restart", () => {
    console.log("Backend has requested a restart");

    toaster.toast({
      title: "SpoofDPI Configuration Updated",
      body: "Your device will automatically restart shortly...",
    })

    setTimeout(() => {
      SteamClient.User.StartRestart(false);
    }, 5000)
  })

  return {
    name: "Decky SpoofDPI",
    titleView: <div className={staticClasses.Title}>Decky SpoofDPI</div>,
    content: <Content />,
    icon: <FaNetworkWired />,
    onDismount() {
      console.log("Unloading")
      removeEventListener("decky_spoof_dpi_needs_restart", restartListener)
    },
  };
});
