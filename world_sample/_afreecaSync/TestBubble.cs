
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

public class TestBubble : UdonSharpBehaviour
{
    public afreecaSync afreecaSync;
    public int 별풍선개수;

    public override void Interact()
    {
        afreecaSync.BubbleEvent(별풍선개수);
    }
}
