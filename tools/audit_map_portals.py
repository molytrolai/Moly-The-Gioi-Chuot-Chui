#!/usr/bin/env python3
"""Audit map portals, NPC lists, and return paths across all available maps."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OVERRIDES_MAP = (
    PROJECT_ROOT
    / "archive"
    / "clients"
    / "local-overrides"
    / "mole.61.com"
    / "resource"
    / "map"
)
MIRROR_MAP = (
    PROJECT_ROOT
    / "archive"
    / "clients"
    / "offline-mirror"
    / "mole.61.com"
    / "resource"
    / "map"
)
COMMUNITY_GRAPH = (
    PROJECT_ROOT
    / "archive"
    / "community"
    / "moleworld.net"
    / "mole2016"
    / "current"
    / "mo-mapgraph.json"
)


def get_map_xml_path(map_id: int) -> Path | None:
    candidates = [
        OVERRIDES_MAP / f"Map_{10000 + map_id}.xml",
        OVERRIDES_MAP / f"Map_{map_id:05d}.xml",
        OVERRIDES_MAP / f"{map_id}.xml",
        MIRROR_MAP / f"Map_{10000 + map_id}.xml",
        MIRROR_MAP / f"Map_{map_id:05d}.xml",
        MIRROR_MAP / f"{map_id}.xml",
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def get_map_swf_path(map_id: int) -> Path | None:
    candidates = [
        OVERRIDES_MAP / f"Map_{10000 + map_id}.swf",
        OVERRIDES_MAP / f"Map_{map_id:05d}.swf",
        OVERRIDES_MAP / f"{map_id}.swf",
        MIRROR_MAP / f"Map_{10000 + map_id}.swf",
        MIRROR_MAP / f"Map_{map_id:05d}.swf",
        MIRROR_MAP / f"{map_id}.swf",
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def audit_maps() -> dict[str, object]:
    graph_data = {}
    if COMMUNITY_GRAPH.is_file():
        try:
            graph_data = json.loads(COMMUNITY_GRAPH.read_text(encoding="utf-8-sig"))
        except Exception:
            pass

    community_maps = set(graph_data.get("maps", {}).keys())

    # Find all available local map IDs
    all_map_ids = set()
    for directory in (OVERRIDES_MAP, MIRROR_MAP):
        if not directory.is_dir():
            continue
        for file in directory.glob("*.*"):
            stem = file.stem.lower()
            if stem.startswith("map_"):
                stem = stem[4:]
            try:
                mid = int(stem)
                if mid >= 10000:
                    mid -= 10000
                all_map_ids.add(mid)
            except ValueError:
                pass

    for mid_str in community_maps:
        try:
            all_map_ids.add(int(mid_str))
        except ValueError:
            pass

    map_details = {}
    missing_assets = []
    dead_ends = []

    for mid in sorted(all_map_ids):
        xml_path = get_map_xml_path(mid)
        swf_path = get_map_swf_path(mid)

        portals = []
        npcs = []
        is_vietnamese = False

        if xml_path and xml_path.is_file():
            try:
                tree = ET.parse(xml_path)
                root = tree.getroot()

                # Parse portals
                for t in root.findall(".//Trigger"):
                    cmd = t.get("Cmd")
                    param = t.get("Param")
                    res = t.get("ResName")
                    tips = t.get("Tips")
                    if cmd == "alt_map" and param:
                        try:
                            target_id = int(param)
                            portals.append({
                                "target": target_id,
                                "res": res,
                                "tips": tips,
                            })
                        except ValueError:
                            pass

                # Parse NPCs
                for n in root.findall(".//Npc"):
                    nid = n.get("ID")
                    name = n.get("Name")
                    npcs.append({"id": nid, "name": name})

                # Check if file has Vietnamese marks
                raw_text = xml_path.read_text(encoding="utf-8", errors="ignore")
                vietnamese_chars = "áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ"
                if any(c in raw_text.lower() for c in vietnamese_chars):
                    is_vietnamese = True

            except Exception as e:
                pass

        has_xml = xml_path is not None
        has_swf = swf_path is not None

        if not has_xml or not has_swf:
            missing_assets.append({
                "map_id": mid,
                "has_xml": has_xml,
                "has_swf": has_swf,
            })

        map_details[mid] = {
            "map_id": mid,
            "has_xml": has_xml,
            "has_swf": has_swf,
            "xml_path": str(xml_path) if xml_path else None,
            "swf_path": str(swf_path) if swf_path else None,
            "portals": portals,
            "npc_count": len(npcs),
            "npcs": npcs,
            "is_vietnamese": is_vietnamese,
        }

    # Analyze return paths
    for mid, details in map_details.items():
        if details["portals"]:
            for p in details["portals"]:
                target = p["target"]
                target_info = map_details.get(target)
                if target_info:
                    # Check if target has a path back
                    return_path = any(
                        tp["target"] == mid for tp in target_info.get("portals", [])
                    )
                    p["has_return"] = return_path
                else:
                    p["has_return"] = False

    return {
        "total_maps": len(map_details),
        "missing_assets_count": len(missing_assets),
        "missing_assets": missing_assets,
        "maps": map_details,
    }


def main() -> None:
    report = audit_maps()
    out = PROJECT_ROOT / "data" / "server" / "map_portal_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Total maps checked: {report['total_maps']}")
    print(f"Maps with missing XML/SWF: {report['missing_assets_count']}")

    # Print summary for primary active maps
    print("\nPrimary route status:")
    for mid in [1, 2, 3, 4, 15, 17, 19, 20, 21, 28, 38, 61, 62, 75, 120, 142, 143]:
        info = report["maps"].get(mid)
        if info:
            destinations = [f"{p['target']}(return={p.get('has_return')})" for p in info['portals']]
            vn = "VIETNAMESE" if info["is_vietnamese"] else "Original"
            print(f"Map {mid:3d}: XML={info['has_xml']}, SWF={info['has_swf']}, NPCs={info['npc_count']:2d}, Lang={vn}, Portals: {destinations}")


if __name__ == "__main__":
    main()
